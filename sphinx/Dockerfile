# Dockerfile for phinx SE
# macbre (c) 2016
FROM debian:sid

# use bash to have 'source' command
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# install dependencies
RUN apt-get update && apt-get install -y sphinxsearch

# set timezone
# @see http://unix.stackexchange.com/a/76711
RUN cp /usr/share/zoneinfo/CET /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

# set up directories
RUN mkdir -pv /opt/sphinx/log /opt/sphinx/index/wbc

# home dir
ENV HOME /opt/sphinx
WORKDIR /opt/sphinx
COPY sphinx.conf /opt/sphinx.conf
