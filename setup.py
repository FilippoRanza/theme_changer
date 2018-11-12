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


from setuptools import setup

setup(
    name='theme_changer',
    version='0.1',
    packages=[''],
    url='https://github.com/FilippoRanza',
    license='GNU General Public License v3.0',
    author='filippo ',
    author_email='',
    description='automatically change wallpaper folder on KDE desktop',
    scripts=['theme_changer.py'],
    install_requires=[
        'pyyaml'
        ]

)
