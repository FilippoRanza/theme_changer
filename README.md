# theme_changer.py [![Build Status](https://travis-ci.com/FilippoRanza/theme_changer.svg?branch=master)](https://travis-ci.com/FilippoRanza/theme_changer)
Automatically change your wallpaper folder on KDE desktop 


## Installation
To install this script you have to run, with root privileges, 
*setup.py install* using python3.

    [sudo] python[3] setup.py install

### Requirements:
    Python 3
    PyYAML 

All those requirements are checked and satisfied  by setup.py

### Configuration:
In order to work properly *theme_changer.py* need a correct configuration
1. Create a directory named *'.wallpapers'* in your home directory. 
You can place your wallpaper collection here or anywhere else.
2. Create a file named *'config.yml'*  in *~/.wallpapers*
3. Fill your configuration file your *seasons*
4. Create a softlink named *'current'* in *~/.wallpapers*. This link should target 
your current wallpaper directory
5. Configure KDE to use *~/.wallpapers/current* as wallpaper location
6. Configure your desktop to autorun *theme_changer.py* at startup. No commands line arguments 
are needed. For example:
    
    

    cd ~/.config/autostart-scripts 
    ln -s $(which theme_changer.py) theme_changer 


#### Dynamic Reconfiguration:
You can add and remove all season that you want any time you want but before it takes effect you must
logout and login to force Plasma to restart. If you run the script during the desktop execution it
will break the softlink and crash the slideshow, if this happens you just have to restart KDE(logout-login).

#### Season Configuration:
A *season* is a YAML entry. It have any kind of fantasy name(but NOT 'default')
 and *must* be unique. Inside each season must be present those three entries:
 1. from *day-month* : defines when a season starts
 2. to  *day-month* : defines when a season ends
 3. dir *path*: define *~/.wallpapers/current* during this season.

There can be any number of *season*, the only *mandatory* season is *default*, that define the behavior
where none of the other season matches.

Default season has just one entry:
1. dir *path*: define *~/.wallpapers/current* when none of the other season matches.

Read 'config.yml' for an example configuration.


