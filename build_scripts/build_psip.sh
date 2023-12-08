


#BUILD PSIP PLUGIN
cd ${SOURCE_DIR}/plugins/psip \
     && rm -rf build \
     && mkdir -p build \
     && cd build \
     && cmake -DInjection_DIR=${VNV_DIR}/lib/cmake -DCMAKE_INSTALL_PREFIX=${SOFTWARE_DIR}/plugins/psip .. \
     && make -j \
     && make install \
     && ${VNV_REGISTER} plugin PSIP ${SOFTWARE_DIR}/plugins/psip/lib/libpsip.so \
     && ${VNV_REGISTER} gui psip ${SOURCE_DIR}/plugins/psip/vnv/config/vnv.__registration__ 

