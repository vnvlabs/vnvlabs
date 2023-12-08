


##BUild the perf plugin

cd ${SOURCE_DIR}/plugins/performance \
     && rm -rf build \
     && mkdir -p build \
     && cd build \
     && cmake -DInjection_DIR=${VNV_DIR}/lib/cmake \
              -DCMAKE_INSTALL_PREFIX=${SOFTWARE_DIR}/plugins/perf .. \
     && make -j \
     && make install \
     && ${VNV_REGISTER} plugin Papi ${SOFTWARE_DIR}/plugins/perf/lib/libpapiTest.so
