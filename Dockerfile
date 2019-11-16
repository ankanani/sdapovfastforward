FROM ubuntu:18.04
MAINTAINER Dax Mickelson (dmickels@cisco.com)

ENV python_script sdapod-fastforward.py

WORKDIR /usr/src/app

# Running APT UPDATE
RUN apt-get -y update

# Running APT DIST-UPGRADE
RUN apt-get -y dist-upgrade

# Running APT AUTOREMOVE
RUN apt-get -y autoremove

# Running APT AUTOCLEAN
RUN apt-get -y autoclean

# Install APT-UTILS
RUN apt-get install -y apt-utils

# Install node.js
RUN apt-get install -y nodejs

# Install npm
RUN apt-get install -y npm

# Install newman
RUN npm install -g newman

# Install Python modules
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY sdapodfastforward.py .
CMD python $python_script
