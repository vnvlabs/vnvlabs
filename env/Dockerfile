


FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
ARG NODE_VERSION=12.18.3

ENV llvm_version=12
ENV TZ=America/New_York
ENV SOURCE_DIR=/home/user/source
ENV SOFTWARE_DIR=/home/user/software
ENV ADIOS_DIR=${SOFTWARE_DIR}/adios
ENV NODE_VERSION=$NODE_VERSION
ENV DEBIAN_FRONTEND=noninteractive 
ENV THEIA_DEFAULT_PLUGINS=local-dir:/theia/plugins
ENV YARN_VERSION=1.22.5
ENV PARAVIEW_DIR=/paraview 
ENV PVPYTHON=${PARAVIEW_DIR}/bin/pvpython 
ENV LLVM_DIR=/usr/lib/llvm-${llvm_version}


RUN apt-get -y update && apt-get -y upgrade && apt-get purge openmpi* && apt-get -y install \
    build-essential \
    wget \
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
    openmpi-bin \
    openmpi-common \
    libopenmpi-dev \
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
    libblas64-3 && pip3 install virtualenv 


#Install cmake
RUN mkdir -p cmake &&\
    cd cmake && \
    wget https://github.com/Kitware/CMake/releases/download/v3.21.3/cmake-3.21.3-linux-x86_64.sh && \
    chmod u+x ./cmake-3.21.3-linux-x86_64.sh &&\
    ./cmake-3.21.3-linux-x86_64.sh --prefix=/usr --skip-license &&\
    cd .. && rm -r ./cmake



#Install llvm
ENV LLVM_DIR=/usr/lib/llvm-${llvm_version}

# -- problems with llvm 12 repo for ubuntu 22.04?
#RUN wget https://apt.llvm.org/llvm.sh && chmod u+x ./llvm.sh && ./llvm.sh ${llvm_version} && rm ./llvm.sh && apt-get install -y libclang-${llvm_version}-dev

RUN apt-get install -y clang-${llvm_version} lldb-${llvm_version} lld-${llvm_version} clangd-${llvm_version} clang-tidy-${llvm_version} clang-format-${llvm_version} clang-tools-${llvm_version} llvm-${llvm_version}-dev lld-${llvm_version} lldb-${llvm_version} llvm-${llvm_version}-tools libomp-${llvm_version}-dev libc++-${llvm_version}-dev libc++abi-${llvm_version}-dev libclang-common-${llvm_version}-dev libclang-${llvm_version}-dev libclang-cpp${llvm_version}-dev libunwind-${llvm_version}-dev


#RUN apt-get purge -y openmpi*


#Install adios
ENV ADIOS_DIR=${SOFTWARE_DIR}/adios
RUN mkdir ${SOFTWARE_DIR} && git clone https://github.com/ornladios/ADIOS2.git ADIOS && mkdir adios2-build && cd adios2-build \
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

#libssl1.1 for mongo db server
RUN echo "deb http://security.ubuntu.com/ubuntu impish-security main" | tee /etc/apt/sources.list.d/impish-security.list
RUN apt-get update && apt-get install libssl1.1

RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/5.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list

RUN apt-get update && apt-get install -y mongodb-org-server  curl wget libsecret-1-dev xz-utils

ARG NODE_VERSION=12.18.3
ENV NODE_VERSION=$NODE_VERSION
ENV DEBIAN_FRONTEND=noninteractive 
ENV THEIA_DEFAULT_PLUGINS=local-dir:/home/theia/plugins
ENV YARN_VERSION=1.22.5

# Install Node.js
RUN ARCH= && dpkgArch="$(dpkg --print-architecture)" \
    && case "${dpkgArch##*-}" in \
    amd64) ARCH='x64';; \
    ppc64el) ARCH='ppc64le';; \
    s390x) ARCH='s390x';; \
    arm64) ARCH='arm64';; \
    armhf) ARCH='armv7l';; \
    i386) ARCH='x86';; \
    *) echo "unsupported architecture"; exit 1 ;; \
    esac \
    && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$ARCH.tar.xz" \
    && tar -xJf "node-v$NODE_VERSION-linux-$ARCH.tar.xz" -C /usr/local --strip-components=1 --no-same-owner \
    && rm "node-v$NODE_VERSION-linux-$ARCH.tar.xz" \
    && ln -s /usr/local/bin/node /usr/local/bin/nodejs \
    &&  curl -fSLO --compressed "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz" \
    && mkdir -p /opt/yarn \
    && tar -xzf yarn-v$YARN_VERSION.tar.gz -C /opt/yarn --strip-components=1 \
    && ln -s /opt/yarn/bin/yarn /usr/local/bin/yarn \
    && ln -s /opt/yarn/bin/yarn /usr/local/bin/yarnpkg \
    && rm yarn-v$YARN_VERSION.tar.gz


#Copy theia config Leave this seperate so we can cache that god awfull thing above. 
COPY theia.package.json /theia/package.json
RUN cd /theia && mkdir plugins \
    && yarn --pure-lockfile && \
    NODE_OPTIONS="--max_old_space_size=4096" yarn theia build && \
    yarn theia download:plugins && \
    yarn --production && \
    yarn autoclean --init && \
    echo *.ts >> .yarnclean && \
    echo *.ts.map >> .yarnclean && \
    echo *.spec.* >> .yarnclean && \
    yarn autoclean --force && \
    yarn cache clean 



