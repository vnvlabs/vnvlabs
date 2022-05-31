


FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
ENV llvm_version=12
ENV TZ=America/New_York
ENV SOURCE_DIR=/source
ENV SOFTWARE_DIR=/software


RUN apt-get -y update && apt-get -y upgrade && apt-get purge openmpi* && apt-get -y install \
    build-essential \
    wget \
    git \
    snap \
    lsb-release \
    software-properties-common \
    zlib1g-dev \
    libssl-dev \
    bzip2 \
    doxygen \
    swig \
    python-dev \
    python3-dev \
    python3-pip \
    libfftw3-dev \
    bear \
    bison \
    flex	\
    gcc\
    g++\
    mpich\
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
RUN wget https://apt.llvm.org/llvm.sh && chmod u+x ./llvm.sh && ./llvm.sh ${llvm_version} && rm ./llvm.sh && apt-get install -y libclang-12-dev 

RUN apt-get purge -y openmpi*


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
    && python build/calc_release_version.py > VERSION_CURRENT \
    && mkdir cmake-build \
    && cd cmake-build \
    && cmake -DENABLE_AUTOMATIC_INIT_AND_CLEANUP=OFF .. \
    && cmake --build . \
    && cmake --build . --target install

RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/5.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list

RUN apt-get update && apt-get install -y mongodb-server  curl wget libsecret-1-dev xz-utils  

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
    && ln -s /usr/local/bin/node /usr/local/bin/nodejs

# Install Yarn
RUN curl -fSLO --compressed "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz" \
    && mkdir -p /opt/yarn \
    && tar -xzf yarn-v$YARN_VERSION.tar.gz -C /opt/yarn --strip-components=1 \
    && ln -s /opt/yarn/bin/yarn /usr/local/bin/yarn \
    && ln -s /opt/yarn/bin/yarn /usr/local/bin/yarnpkg \
    && rm yarn-v$YARN_VERSION.tar.gz

#Copy theia config
WORKDIR /theia
COPY theia.package.json package.json

# Build Theia
RUN yarn --pure-lockfile && \
    NODE_OPTIONS="--max_old_space_size=4096" yarn theia build && \
    yarn theia download:plugins && \
    yarn --production && \
    yarn autoclean --init && \
    echo *.ts >> .yarnclean && \
    echo *.ts.map >> .yarnclean && \
    echo *.spec.* >> .yarnclean && \
    yarn autoclean --force && \
    yarn cache clean 

WORKDIR /

#Install Pavaview server (used for visualization) 
RUN wget -O pv.tar.gz "https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.10&type=binary&os=Linux&downloadFile=ParaView-5.10.1-osmesa-MPI-Linux-Python3.9-x86_64.tar.gz"   
RUN tar -xf pv.tar.gz && mv ParaView-5.10.1-osmesa-MPI-Linux-Python3.9-x86_64 paraview && rm pv.tar.gz 

ENV PARAVIEW_DIR=/paraview 
ENV PVPYTHON=${PARAVIEW_DIR}/bin/pvpython 

#Install vim for text editing. 
RUN apt-get install -y vim 

#Install Dakota
#RUN wget https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.14.0-release-public-src-cli.tar.gz
#RUN tar -xf dakota-6.14.0-release-public-src-cli.tar.gz
#RUN apt-get install
#RUN cd dakota-6.14.0.src/ && mkdir build && cd build && cmake \
#  -D CMAKE_C_FLAGS="-O2"\
#  -D CMAKE_CXX_FLAGS="-O2"\
#  -D CMAKE_Fortran_FLAGS="-O2"\
#  -D DAKOTA_HAVE_GSL:BOOL=TRUE\
#  -D HAVE_QUESO:BOOL=TRUE\
#  -D DAKOTA_HAVE_MPI:BOOL=TRUE \
#  -D DAKOTA_HDF5:BOOL=TRUE\
#  -DBoost_NO_BOOST_CMAKE:BOOL=TRUE .. && make && make install
