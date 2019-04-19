#! /usr/bin/python

import os
from os.path import isdir, isfile

from shutil import copyfile

from random import randint, choices, random
from string import ascii_letters

from theme_changer import Config, check_config, load_config, DEF_CONF_FILE, DEF_CONF_DIR


DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
assert sum(DAYS) == 365


def date_to_str(d):
    return "%d-%d" % d


def date_generator():
    for i, m in enumerate(range(1, 13)):
        for d in range(1, DAYS[i]+1):
            yield (d, m), date_to_str((d, m))


def before(a, b):
    return a[1] < b[1] or (a[1] == b[1] and a[0] < b[0])


def config_generator():
    for f, fs in date_generator():
        for t, ts in date_generator():
            conf = {'from': fs, 'to': ts, 'dir': ''}
            yield (f, t, conf)


def test_date_parser():
    for f, t, c in config_generator():
        conf = Config(c)
        if f != t:
            assert conf.start_date < conf.end_date
            if before(f, t):
                assert conf.start_date.year == conf.end_date.year
            else:
                assert (conf.start_date.year + 1) == conf.end_date.year
        else:
            assert conf.start_date == conf.end_date


def rand_date():
    month = randint(0, len(DAYS)-1)
    day = randint(1, DAYS[month])
    return f'{day}-{month + 1}'


def rand_str():
    size = randint(1, 100)
    tmp = choices(ascii_letters, k=size)
    return ''.join(tmp)


def make_correct_rand_season():
    conf = {}
    conf['from'] = rand_date()
    conf['to'] = rand_date()
    conf['dir'] = os.getcwd()
    return conf


def make_wrong_rand_season():
    conf = {}
    if random() < 0.5:
        conf['from'] = rand_date() 
    else:
        conf['from'] = rand_str() 

    if random() < 0.5:
        conf['to'] = rand_date() 
    else:
        conf['to'] = rand_str() 

    if random() < 0.5:
        conf['dir'] = os.getcwd()
    else:
        conf['dir'] = rand_str() 

    return conf


def make_config(callback):
    out = {}
    size = randint(10, 100)
    for i in range(size):
        name = rand_str()
        if name == 'default':
            continue
        out[name] = callback()

    out['default'] = {
        'dir' : os.getcwd()
    }
    
    return out


def test_check_config():
    f = lambda x: x
    correct = make_config(make_correct_rand_season)
    assert check_config(correct, f)

    for i in range(1000):
        wrong = make_config(make_wrong_rand_season)
        assert not check_config(wrong, f)


def test_load_config():

    if not isdir(DEF_CONF_DIR):
        os.mkdir(DEF_CONF_DIR)
    
    if not isfile(DEF_CONF_FILE):
        copyfile('config.yml', DEF_CONF_FILE)

    try:
       conf = load_config()
    except:
        assert False
    else:
        assert type(conf) == dict
        assert True
