


FROM ubuntu:20.04

ENV llvm_version=12
ENV TZ=America/New_York
ENV DEBIAN_FRONTEND=noninteractive 
ENV SOURCE_DIR=/source
ENV SOFTWARE_DIR=/software
ENV LLVM_DIR=/usr/lib/llvm-${llvm_version}
ENV VNV_HOME_PATH=/software

RUN apt-get -y update && apt-get -y upgrade && apt-get purge openmpi* && apt-get -y install \
    build-essential \
    wget \
    curl \
    vim \
    git \
    snap \
    lsb-release \
    software-properties-common \
    zlib1g-dev \
    libssl-dev \
    bzip2 \
    doxygen \
    swig \
    python3-dev \
    python3-pip \
    libfftw3-dev \
    bear \
    bison \
    flex	\
    gcc\
    g++\
    mpich \
    libmpich-dev \
    gfortran\
    libboost-all-dev \
    libblas-dev \
    liblapack-dev \
    gsl-bin \
    libgsl-dev \
    libomp-dev \
    perl \
    libmicrohttpd-dev \
    libglapi-mesa \
    gdb \
    valgrind \
    pkg-config \
    libsecret-1-dev \
    libblas64-3

#Install cmake
RUN mkdir -p cmake &&\
    cd cmake && \
    wget https://github.com/Kitware/CMake/releases/download/v3.21.3/cmake-3.21.3-linux-x86_64.sh && \
    chmod u+x ./cmake-3.21.3-linux-x86_64.sh &&\
    ./cmake-3.21.3-linux-x86_64.sh --prefix=/usr --skip-license &&\
    cd .. && rm -r ./cmake

#Install llvm
RUN wget https://apt.llvm.org/llvm.sh && chmod u+x ./llvm.sh && ./llvm.sh ${llvm_version} && rm ./llvm.sh && apt-get install -y libclang-${llvm_version}-dev

RUN apt-get purge -y openmpi*

#Install PAPI (used in the plugins)
RUN git clone https://github.com/icl-utk-edu/papi.git &&  cd papi/src && ./configure && make && make install  

