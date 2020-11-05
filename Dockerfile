FROM nvidia/cuda:11.0-cudnn8-runtime-ubuntu18.04
LABEL maintainer Artem Baraniuk "artem.baranyuk@gmail.com"

# Define environmental variables
ENV BUILD_PACKAGES mc git cmake wget nano unzip build-essential pkg-config gcc g++
ENV PYTHON_SYSTEM_PACKAGES python3 python3-dev python3-pip python3-setuptools python3-venv
ENV OPENCV_PACKAGES libavcodec-dev libavformat-dev libswscale-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev \
                    libgtk-3-dev libpng-dev libjpeg-dev
ENV X11_PACKAGES libxkbcommon-dev libxcb-xkb-dev
ENV PYTHON_PACKAGES numpy scipy torch torchvision matplotlib Pillow scikit-image flask pytest pytest-cov scipy \
                    Werkzeug eventlet


# Install system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    $BUILD_PACKAGES $PYTHON_SYSTEM_PACKAGES $OPENCV_PACKAGES $X11_PACKAGES && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Install python packages
RUN pip3 install $PYTHON_PACKAGES


# Install OpenCV
RUN git clone https://github.com/opencv/opencv.git && \
    cd opencv && mkdir build && cd build && \
    cmake \
      -D CMAKE_BUILD_TYPE=Release \
      -D CMAKE_INSTALL_PREFIX=/usr \
      -D BUILD_PNG=ON  -D BUILD_TIFF=OFF   -D BUILD_TBB=OFF \
      -D BUILD_JPEG=ON -D BUILD_JASPER=OFF -D BUILD_ZLIB=OFF \
      -D BUILD_opencv_java=OFF  \
      -D BUILD_opencv_python2=OFF  -D BUILD_opencv_python3=ON \
      -D WITH_CUDA=OFF  -D WITH_CUBLAS=OFF \
      -D CUDA_FAST_MATH=OFF \
      -D BUILD_TESTS=OFF \
      -D WITH_OPENCL=OFF  -D WITH_OPENMP=OFF   -D WITH_FFMPEG=ON \
      -D WITH_GSTREAMER=OFF  -D WITH_GSTREAMER_0_10=OFF  -D WITH_GTK=ON \
      -D WITH_VTK=OFF  -D WITH_TBB=ON  -D WITH_1394=OFF  -D WITH_OPENEXR=OFF .. && \
    make -j$(nproc --ignore=1) && make install && \
    cd / && rm -rf opencv/

EXPOSE 5000
