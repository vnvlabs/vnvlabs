


#BUILD MOOSE
cd ${SOURCE_DIR}/applications/moose/framework\
   && make clean \
   && bear make -j 8 \
   && ${VNV_MATCHER} --package MOOSE\
                      --fix-omp \
  		              --cache vnv.__cache__\
    		          --output src/utils/vnv_MOOSE.C \
                      compile_commands.json \
   && make -j \
   && python3 /vnvlabs/build_scripts/utils/run_in_subdirs.py ${SOURCE_DIR}/applications/moose/examples make vnv \
   && ${VNV_REGISTER} gui moose ${SOURCE_DIR}/applications/moose/vnv/gui/vnv.__registration__ 

