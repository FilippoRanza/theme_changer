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
Automatically change your wallpaper folder on KDE desktop
"""
from os import symlink, readlink, remove, chdir
from os.path import join, isdir, abspath, exists, isfile

import sys
from argparse import ArgumentParser

from datetime import datetime
import re

from syslog import syslog
from pathlib import Path

import yaml


# define working directory and configuration file
# ignore IDE warning, this works perfectly
DEF_CONF_DIR = join(Path.home(), '.wallpaper')
DEF_CONF_FILE = join(DEF_CONF_DIR, 'config.yml')
DEF_WALLPAPER_LINK = 'current'

# configuration file keywords
KEY_WORDS = ['from', 'to', 'dir']
DATE_RE = re.compile(r'\d?\d-\d?\d')


class Config:
    """
    contain the parsed configuration
    in a ready to used format
    """
    def __init__(self, conf):
        self.start_date = datetime.strptime(conf['from'], r'%d-%m')
        self.end_date = datetime.strptime(conf['to'], r'%d-%m')
        self.directory = conf['dir']
        self._set_year_()


    def _set_year_(self):
        """
        set the correct year to
        each date.
        """
        year = datetime.now().year
        if self.end_date < self.start_date:
            self.end_date = self.end_date.replace(year=year + 1)
        else:
            self.end_date = self.end_date.replace(year=year)
        self.start_date = self.start_date.replace(year=year)

    def inside_range(self, date):
        """
        check the given date is inside [start_date, end_date]
        range
        """
        return self.start_date <= date <= self.end_date


def load_config():
    """
    read and parse 'config.yml'
    """
    with open(DEF_CONF_FILE) as file:
        out = yaml.safe_load(file)
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

    for key, value in conf.items():
        if key not in KEY_WORDS:
            log('%s is an unknown keyword' % key)
            return False

        if key == 'dir':
            if not isdir(value):
                log('%s is not a directory' % value)
                return False
        else:
            if not DATE_RE.fullmatch(value):
                log('%s does not match the day-month pattern' % value)
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

    for key, value in conf.items():
        if key == 'default':
            status = check_default(value)
        else:
            status = check_season(value, log)
        if not status:
            return False
    return True


def parse_config(conf):
    """
    extract information from the configuration
    """
    out = {}
    for key, value in conf.items():
        if key != 'default':
            out[key] = Config(value)
        else:
            out[key] = value['dir']
    return out


def run_config(conf):
    """
    find the current theme
    """
    today = datetime.now()
    parse = parse_config(conf)
    for key, value in parse.items():
        if key != 'default':
            if value.inside_range(today):
                folder = abspath(value.d)
                theme = key
                break
    else:
        theme = 'default'
        folder = parse[theme]

    return folder, theme


def change_theme(folder, theme, log):
    """
    change the soft link's target
    """
    if not exists(DEF_WALLPAPER_LINK):
        symlink(folder, DEF_WALLPAPER_LINK)
        log('Create %s' % DEF_WALLPAPER_LINK)
    else:
        curr = readlink(DEF_WALLPAPER_LINK)
        if curr != folder:
            remove(DEF_WALLPAPER_LINK)
            symlink(folder, DEF_WALLPAPER_LINK)
            log('Change theme to %s' % theme)


def check_env(log):
    """
    check that the file system have the
    correct files
    """
    if not isdir(DEF_CONF_DIR):
        log('missing configuration directory [%s]' % DEF_CONF_DIR)
    elif not isfile(DEF_CONF_FILE):
        log('missing configuration file [%s]' % DEF_CONF_FILE)
    else:
        chdir(DEF_CONF_DIR)
        return True
    return False


def init_argparser():
    """
    configure the argument parser
    """
    out = ArgumentParser(
        description='Automatically change your wallpaper folder on KDE desktop')
    out.add_argument(
        '-c', '--check', help='check configuration file, without run the theme changer',
        default=False, action='store_true')

    out.add_argument(
        '-d', '--dry', help='execute a dry run: simply print out current theme without change it',
        default=False, action='store_true'
    )

    return out


def run_check():
    """
    just run the  check of the
    configuration file
    """
    if check_env(print):
        config = load_config()
        check_config(config, print)


def run_theme_changer(dry=False):
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
        if dry:
            print(dir_path, theme)
        else:
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
        run_theme_changer(args.dry)


if __name__ == '__main__':
    main()
