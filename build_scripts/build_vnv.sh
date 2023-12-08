

# install vnv toolkit
cd ${SOURCE_DIR}/vnv  \
    && rm -rf build \
    && mkdir -p build \
    && cd build \
    && cmake -DCMAKE_INSTALL_PREFIX=${VNV_DIR} -DLLVM_DIR=${LLVM_DIR} .. \
    && make -j 8 \
    && make install 

# Register the vnv toolkit.
${VNV_REGISTER} gui VnV ${SOURCE_DIR}/vnv/gui/vnv-config.json
