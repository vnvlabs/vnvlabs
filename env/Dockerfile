


FROM ubuntu:20.04

ENV llvm_version=12
ENV TZ=America/New_York
ENV DEBIAN_FRONTEND=noninteractive 
ENV SOURCE_DIR=/home/user/source
ENV SOFTWARE_DIR=/home/user/software
ENV ADIOS_DIR=${SOFTWARE_DIR}/adios
ENV LLVM_DIR=/usr/lib/llvm-${llvm_version}

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
    libblas64-3 && pip3 install virtualenv  

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

#Install adios
RUN mkdir -p ${SOFTWARE_DIR} && git clone https://github.com/ornladios/ADIOS2.git ADIOS && mkdir adios2-build && cd adios2-build \
  && cmake -DCMAKE_INSTALL_PREFIX=${ADIOS_DIR} ../ADIOS && make -j 16 && make install && cd .. && rm -r adios2-build \
  && rm -r ADIOS 


#Install PAPI (used in the plugins)
RUN git clone https://bitbucket.org/icl/papi.git &&  cd papi/src && ./configure && make && make install  


# mongo db is broken in apt -- install from source.
RUN git clone https://github.com/mongodb/mongo-c-driver.git \
    && cd mongo-c-driver \
    && git checkout 1.20.1 \
    && python3 build/calc_release_version.py > VERSION_CURRENT \
    && mkdir cmake-build \
    && cd cmake-build \
    && cmake -DENABLE_AUTOMATIC_INIT_AND_CLEANUP=OFF .. \
    && cmake --build . \
    && cmake --build . --target install


RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add - 
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
RUN apt-get update && apt-get install -y mongodb-org



