


#BUILD SWFFT
# install swfft with VnV
cd ${SOURCE_DIR}/applications/swfft \
    && make clean \
    && bear make -j \
    && ${VNV_MATCHER} --package SWFFT\
                      --output reg_SWFFT.cpp\
                      --cache vnv.__cache__\
		              --fix-omp \
 		              compile_commands.json \
    && ${VNV_MATCHER} --package TestDFFT\
                      --output reg_TestDFFT.cpp\
                      --cache vnv.__cache__\
		              --targetFile $PWD/build/TestDFFT \
	                  compile_commands.json\
    && make \
    && ${VNV_REGISTER} gui swfft ${SOURCE_DIR}/applications/swfft/vnv/gui/vnv.__registration__ 
