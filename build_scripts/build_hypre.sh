



#Build hypre with vnv
cd ${SOURCE_DIR}/applications/hypre/src \
    && rm -rf build \
    && mkdir -p build \
    && cd build \
    && cmake -DHYPRE_ENABLE_BIGINT=1\
             -DHYPRE_ENABLE_SHARED=1\
             -DHYPRE_ENABLE_VNV=1\
             -DHYPRE_BUILD_EXAMPLES=1\
	         -DCMAKE_EXPORT_COMPILE_COMMANDS=ON\
	         -DCMAKE_INSTALL_PREFIX=${HYPRE_DIR}\
             -DInjection_DIR=${VNV_DIR}/lib/cmake .. \
   && cmake .. \
   && make -j \
   && make install \
   && ${VNV_REGISTER} gui hypre ${SOURCE_DIR}/applications/hypre/vnv/gui/vnv.__registration__ 
