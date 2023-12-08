

#BUILD SIMPLE
cd ${SOURCE_DIR}/applications/simple \
     && rm -rf build \
     && mkdir -p build \
     && cd build \
     && cmake -DInjection_DIR=${VNV_DIR}/lib/cmake -DCMAKE_INSTALL_PREFIX=${SOFTWARE_DIR}/simple .. \
     && make -j \
     && make install  \
     && ${VNV_REGISTER} gui simple ${SOURCE_DIR}/applications/simple/vnv/config/vnv.__registration__ 

