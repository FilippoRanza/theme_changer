#! /usr/bin/python
#
#  theme_changer.py - Automatically change your wallpaper folder on KDE desktop
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Test for theme_changer.py
"""
import os
from os.path import isdir, isfile

from shutil import copyfile

from random import randint, choices, random
from string import ascii_letters

from yaml.parser import ParserError

from theme_changer import Config, check_config, load_config, DEF_CONF_FILE, DEF_CONF_DIR


DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
assert sum(DAYS) == 365


def date_to_str(date):
    """
    convert from tuple to string
    """
    return "%d-%d" % date


def date_generator():
    """
    enumerate all possible day-month (365)
    """
    for i, month in enumerate(range(1, 13)):
        for day in range(1, DAYS[i]+1):
            yield (day, month), date_to_str((day, month))


def before(date_a, date_b):
    """
    check is (day, month) inside a is
    before (day, month) inside b
    """
    day_a, month_a = date_a
    day_b, month_b = date_b

    return month_a < month_b or (month_a == month_b and day_a < day_b)


def config_generator():
    """
    enumerate all possible day-month configurations
    (365 * 365)
    """
    for start_date, start_date_str in date_generator():
        for end_date, end_date_str in date_generator():
            conf = {'from': start_date_str, 'to': end_date_str, 'dir': ''}
            yield (start_date, end_date, conf)


def test_date_parser():
    """
    test the Config class: it must
    guess the correct year to compute
    the correct date range
    """
    for start_date, end_date, config in config_generator():
        conf = Config(config)
        if start_date != end_date:
            assert conf.start_date < conf.end_date
            if before(start_date, end_date):
                assert conf.start_date.year == conf.end_date.year
            else:
                assert (conf.start_date.year + 1) == conf.end_date.year
        else:
            assert conf.start_date == conf.end_date


def rand_date():
    """
    generate a string containing a correct
    day-month date
    """
    month = randint(0, len(DAYS)-1)
    day = randint(1, DAYS[month])
    return f'{day}-{month + 1}'


def rand_str():
    """
    generate a random string made out of ascii
    letters
    """
    size = randint(1, 100)
    tmp = choices(ascii_letters, k=size)
    return ''.join(tmp)


def make_correct_rand_season():
    """
    Generate a correct season
    """
    conf = {}
    conf['from'] = rand_date()
    conf['to'] = rand_date()
    conf['dir'] = os.getcwd()
    return conf


def make_wrong_rand_season():
    """
    Generare a season with errors
    """
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
    """
    Generate a configuation
    dictionary. Its content is
    generated by 'callback'
    """
    out = {}
    size = randint(10, 100)
    for _ in range(size):
        name = rand_str()
        if name == 'default':
            continue
        out[name] = callback()

    out['default'] = {
        'dir' : os.getcwd()
    }

    return out


def test_check_config():
    """
    run the configuation checker on
    correct and wrong configurations
    """
    empty_callback = lambda x: x
    correct = make_config(make_correct_rand_season)
    assert check_config(correct, empty_callback)

    for _ in range(1000):
        wrong = make_config(make_wrong_rand_season)
        assert not check_config(wrong, empty_callback)


def test_load_config():

    """
    ensure that the loading actually works
    """

    if not isdir(DEF_CONF_DIR):
        os.mkdir(DEF_CONF_DIR)

    if not isfile(DEF_CONF_FILE):
        copyfile('config.yml', DEF_CONF_FILE)

    try:
        conf = load_config()
    except ParserError:
        assert False
    else:
        assert isinstance(conf, dict)
        assert True
