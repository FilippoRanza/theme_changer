#! /usr/bin/python
from datetime import datetime
import os
from subprocess import call
from theme_changer import Config


name = 'theme_changer.py'

days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
assert sum(days) == 365


def exist():
    path = os.environ.get('PATH')
    if path is None:
        return False

    for d in path.split(':'):
        for f in os.scandir(d):
            if f.name == name:
                return True
    return False


def date_to_str(d):
    return "%d-%d" % d


def date_generator():
    for i, m in enumerate(range(1, 13)):
        for d in range(1, days[i]+1):
            yield (d, m), date_to_str((d, m))


def before(a, b):
    return a[1] < b[1] or (a[1] == b[1] and a[0] < b[0])


def config_generator():
    for f, fs in date_generator():
        for t, ts in date_generator():
            conf = {'from': fs, 'to': ts, 'dir': ''}
            yield (f, t, conf)


def test_installation():
    assert exist()
    try:
        a = call(name)
    except FileNotFoundError:
        a = -1
    except PermissionError:
        a = -1
    # script execution will fail: the system is not configured
    assert a != -1


def test_date_parser():
    today = datetime.now()
    for f, t, c in config_generator():
        conf = Config(c)
        if f != t:
            assert conf.f < conf.t
            if before(f, t):
                assert conf.f.year == conf.t.year
            else:
                assert (conf.f.year + 1) == conf.t.year
                tmp = Config.make_date(c['from'])
                if today < tmp:
                    assert conf.f.year == (today.year - 1)
                    assert conf.t.year == today.year
                else:
                    assert conf.f.year == today.year
                    assert conf.t.year == (today.year + 1)

        else:
            assert conf.f == conf.t
