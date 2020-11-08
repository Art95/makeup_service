FROM nvidia/cuda:11.0-cudnn8-runtime-ubuntu18.04
LABEL maintainer Artem Baraniuk "artem.baranyuk@gmail.com"

# Define environmental variables
ENV BUILD_PACKAGES mc git cmake wget nano unzip build-essential pkg-config gcc g++
ENV PYTHON_SYSTEM_PACKAGES python3 python3-dev python3-pip python3-setuptools python3-venv
ENV OPENCV_PACKAGES libavcodec-dev libavformat-dev libswscale-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev \
                    libgtk-3-dev libpng-dev libjpeg-dev
ENV X11_PACKAGES libxkbcommon-dev libxcb-xkb-dev


# Install system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    $BUILD_PACKAGES $PYTHON_SYSTEM_PACKAGES $OPENCV_PACKAGES $X11_PACKAGES && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 8081

# IMPORTANT: Copy /etc/protocols to folder with Dockerfile to execute this. Needed for tcp to work
COPY ./protocols /etc/protocols

# Install project related dependencies
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt && rm /requirements.txt
