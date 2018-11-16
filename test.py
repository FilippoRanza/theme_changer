#! /usr/bin/python

import os
from subprocess import call

name = 'theme_changer.py'


def exist():
    path = os.environ.get('PATH')
    if path is None:
        return False

    for d in path.split(':'):
        for f in os.scandir(d):
            if f.name == name:
                return True
    return False


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

