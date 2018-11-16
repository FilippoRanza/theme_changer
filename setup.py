#! /usr/bin/python

#
#  theme_changer.py - Automatically change your wallpaper folder on KDE desktop
#                   - installation script
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

import sys
from setuptools import setup
# you can't install with python2
assert sys.version_info.major == 3, 'theme_changer.py needs python3'

setup(
    name='theme_changer',
    version='0.1',
    packages=[''],
    url='https://github.com/FilippoRanza/theme_changer',
    license='GNU General Public License v3.0',
    author='Filippo Ranza',
    author_email='filipporanza@gmail.com',
    description='automatically change wallpaper folder on KDE desktop',
    scripts=['theme_changer.py'],
    install_requires=[
        'pyyaml'
        ]

)
