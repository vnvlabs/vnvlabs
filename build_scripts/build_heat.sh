

#BUild heat equation

cd ${SOURCE_DIR}/applications/heat \
     && rm -rf build \
     && mkdir -p build \
     && cd build \
     && cmake -DInjection_DIR=${VNV_DIR}/lib/cmake .. -DCMAKE_INSTALL_PREFIX=${SOFTWARE_DIR}/heat \
     && make -j \
     && make install  \
     && ${VNV_REGISTER} gui heat ${SOURCE_DIR}/applications/heat/vnv/gui/vnv.__registration__ 


