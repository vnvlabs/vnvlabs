
##BUILD ASGARD
#Install asgard directly into the software dir as they dont have a install target.
cd ${SOURCE_DIR}/applications/asgard \
    && rm -rf build \
    && mkdir -p build \
    && cd build \
    && cmake -DInjection_DIR=${VNV_DIR}/lib/cmake -DASGARD_USE_VNV=ON .. \
    && make -j \
    && ${VNV_REGISTER} gui asgard ${SOURCE_DIR}/applications/asgard/vnv/config/vnv.__registration__ 

