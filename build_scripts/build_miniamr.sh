



#Build MINIAMR
cd ${SOURCE_DIR}/applications/miniamr/ref \
    && make clean \
    && bear make -j \
    && ${VNV_DIR}/bin/vnv-matcher --package MINIAMR \
                                  --output vnv_MINIAMR.c\
                         		  --fix-omp \
				                  --targetFile ${PWD}/miniAMR.x \
				                  --cache vnv.__cache__\
                                  compile_commands.json\
    && make -j \
    && ${VNV_REGISTER} gui miniAMR ${SOURCE_DIR}/applications/miniamr/vnv/gui/vnv.__registration__ 
