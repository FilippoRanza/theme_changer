# This container, and Docker in general,  is NOT needed to run
# 'theme_changer'.
# It is here just to test the installation script.

FROM ubuntu

RUN ["apt", "update"]
RUN ["apt", "upgrade", "-y"]

RUN ["apt", "install", "python3", "-y"]
RUN ["apt", "install", "python3-setuptools", "-y"]
RUN ["apt", "install", "git", "-y"]

RUN ["git", "clone", "https://github.com/FilippoRanza/theme_changer.git"]
WORKDIR "theme_changer"
RUN ["python3", "setup.py", "install"]

RUN ["which", "theme_changer.py"]


