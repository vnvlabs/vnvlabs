



#Build the issues plugin
#Install the simple application example. 
cd ${SOURCE_DIR}/plugins/issues \
     && rm -rf build \
     && mkdir -p build \
     && cd build \
     && cmake -DInjection_DIR=${VNV_DIR}/lib/cmake -DCMAKE_INSTALL_PREFIX=${SOFTWARE_DIR}/plugins/issues .. \
     && make -j \
     && make install \
     && ${VNV_REGISTER} plugin ISSUES ${SOFTWARE_DIR}/plugins/issues/lib/libissues.so \
     && ${VNV_REGISTER} gui ISSUES ${SOURCE_DIR}/plugins/issues/vnv/config/vnv.__registration__


