

# Wrapper around bear that injects the openmp include directory.
cd ${SOURCE_DIR}/applications/xsbench/openmp-threading \
    && rm -rf build \
    && bear make -j \
    && ${VNV_MATCHER} --package XSBENCH \
                      --output Registration_XSBENCH.c \
                      --fix-omp \
                      --cache vnv.__cache__ \
                      --targetFile ${PWD}/XSBench \
                      compile_commands.json\
    && make -j \
    && ${VNV_REGISTER} gui xs-bench ${SOURCE_DIR}/applications/xsbench/vnv/gui/vnv.__registration__ 




