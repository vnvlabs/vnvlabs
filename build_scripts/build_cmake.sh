


#Install cmake
mkdir -p cmake &&\
    cd cmake && \
    wget https://github.com/Kitware/CMake/releases/download/v3.21.3/cmake-3.21.3-linux-x86_64.sh && \
    chmod u+x ./cmake-3.21.3-linux-x86_64.sh &&\
    ./cmake-3.21.3-linux-x86_64.sh --prefix=/usr --skip-license &&\
    cd .. && rm -r ./cmake
