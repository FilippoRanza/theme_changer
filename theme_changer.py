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


import yaml
import os
from datetime import datetime
from os import path
import re
from syslog import syslog
import sys
from argparse import ArgumentParser
from pathlib import Path


# define working directory and configuration file
# ignore IDE warning, this works perfectly
DEF_CONF_DIR = path.join(Path.home(), '.wallpaper')
DEF_CONF_FILE = path.join(DEF_CONF_DIR, 'config.yml')
DEF_WALLPAPER_LINK = 'current'

# configuration file keywords
KEY_WORDS = ['from', 'to', 'dir']
date_re = re.compile(r'\d?\d-\d?\d')


# Current date and year
TODAY = datetime.now()
YEAR = TODAY.year


class Config:
    """
    contain the parsed configuration
    in a ready to used format
    """
    def __init__(self, conf):
        self.f = Config.make_date(conf['from'])
        self.t = Config.make_date(conf['to'])
        self.d = conf['dir']
        self._set_year_()

    @staticmethod
    def make_date(date):
        out = datetime.strptime(date, '%d-%m')
        return out.replace(year=YEAR)

    def _set_year_(self):
        """
        set the correct year to
        each date.
        """
        # if 'to' is previous then 'from',
        # those dates are not in the same year
        if self.t < self.f:
            # if 'from' is in the future, it must be relative to the past year
            if TODAY < self.f:
                self.f = self.f.replace(year=YEAR - 1)
            # otherwise 'to' is in the future
            else:
                self.t = self.t.replace(year=YEAR + 1)


def load_config():
    """
    read and parse 'config.yml'
    """
    with open(DEF_CONF_FILE) as f:
        out = yaml.load(f)
    return out


def check_default(conf):
    """
    check that the 'default' theme is
    correctly configured
    """
    return len(conf) == 1 and 'dir' in conf


def check_season(conf, log):
    """
    check that the custom theme
    is correctly configured
    """
    if len(conf) != 3:
        return False
    for k, v in conf.items():
        if k not in KEY_WORDS:
            log('%s is an unknown keyword' % k)
            return False
        else:
            if k == 'dir':
                if not path.isdir(v):
                    log('%s is not a directory' % v)
                    return False
            else:
                if not date_re.fullmatch(v):
                    log('%s does not match the day-month pattern' % v)
                    return False

    return True


def check_config(conf, log):
    """
    check that the whole configuration is
    correct
    """
    if 'default' not in conf:
        log('config.yml must have a "default" section')
        return False

    for k, v in conf.items():
        if k == 'default':
            s = check_default(v)
        else:
            s = check_season(v, log)
        if not s:
            return False
    return True


def parse_config(conf):
    """
    extract information from the configuration
    """
    out = {}
    for k, v in conf.items():
        if k != 'default':
            out[k] = Config(v)
        else:
            out[k] = v['dir']
    return out


def run_config(conf):
    """
    find the current theme
    """
    parse = parse_config(conf)
    for k, v in parse.items():
        if k != 'default':
            if v.f <= TODAY <= v.t:
                p = path.abspath(v.d)
                t = k
                break
    else:
        t = 'default'
        p = parse[t]

    return p, t


def change_theme(p, t, log):
    """
    change the soft link's target
    """
    if not path.exists(DEF_WALLPAPER_LINK):
        os.symlink(p, DEF_WALLPAPER_LINK)
        log('Create %s' % DEF_WALLPAPER_LINK)
    else:
        curr = os.readlink(DEF_WALLPAPER_LINK)
        if curr != p:
            os.remove(DEF_WALLPAPER_LINK)
            os.symlink(p, DEF_WALLPAPER_LINK)
            log('Change theme to %s' % t)


def check_env(log):
    """
    check that the file system have the
    correct files
    """
    if not path.isdir(DEF_CONF_DIR):
        log('missing configuration directory [%s]' % DEF_CONF_DIR)
    elif not path.isfile(DEF_CONF_FILE):
        log('missing configuration file [%s]' % DEF_CONF_FILE)
    else:
        os.chdir(DEF_CONF_DIR)
        return True
    return False


def init_argparser():
    """
    configure the argument parser
    """
    out = ArgumentParser(description=' Automatically change your wallpaper folder on KDE desktop')
    out.add_argument('-c', '--check', help='check configuration file, without run the theme changer',
                     default=False, action='store_true')

    return out


def run_check():
    """
    just run the  check of the
    configuration file
    """
    if check_env(print):
        config = load_config()
        check_config(config, print)


def run_theme_changer():
    """
    run the check of the configuration file
    and change theme, if needed
    """
    log = syslog
    if not check_env(log):
        sys.exit(2)

    config = load_config()
    if check_config(config, log):
        dir_path, theme = run_config(config)
        change_theme(dir_path, theme, log)
    else:
        log('theme_changer.py configuration file[%s] contains errors' % DEF_CONF_FILE)


def main():
    """
    run the script:
        - parse the CLI argument
        - run the given command
    """
    parse = init_argparser()
    args = parse.parse_args()
    if args.check:
        run_check()
    else:
        run_theme_changer()


if __name__ == '__main__':
    main()

