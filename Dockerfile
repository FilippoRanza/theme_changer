# This container, and Docker in general,  is NOT needed to run
# 'theme_changer'.
# It is here just to test the installation script.

FROM Ubuntu

RUN ["apt", "update"]
RUN ["apt", "upgrade"]

RUN ["apt", "install", "python3"]
RUN ["apt", "install", "python3-setuptools"]
RUN ["apt", "install", "git"]

RUN ["git", "clone", "https://github.com/FilippoRanza/theme_changer.git"]
RUN ["cd", "theme_changer"]
RUN ["python3", "setup.py", "install"]

RUN ["which", "theme_changer.py"]


