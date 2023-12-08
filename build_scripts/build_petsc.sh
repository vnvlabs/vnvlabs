
unset PETSC_DIR
unset PETSC_ARCH 

#Build PETSC
cd ${SOURCE_DIR}/applications/petsc \
     && ./configure --prefix=${SOFTWARE_DIR}/petsc \
                    --with-hypre-dir=${HYPRE_DIR}\
                    --with-vnv-dir=${VNV_DIR}\
                    --with-debugging=no\
                    --with-shared-libraries=1\
                    --download-fblaslapack=1\
                    --download-metis=1\
                    --download-ptscotch=1\
                    --download-parmetis=1\
                    --download-superlu_dist=1\
                    --download-mumps=1\
                    --download-strumpack=1\
                    --download-scalapack=1\
                    --download-slepc=1 \
                    --with-mpi=1 \
                    --with-cxx-dialect=C++11 \
                    --with-fortran-bindings=0\
                    --with-sowing=0 \
                    --with-64-bit-indices \
     && bear make -j \
     && ${VNV_MATCHER} --package PETSC \
                        --output src/sys/vnv/vnv_PETSC.c \
                        --cache src/sys/vnv/vnv.__cache__ \
                        --fix-omp \
			compile_commands.json \
     && make -j \
     && make install \
     && ${VNV_REGISTER} gui petsc ${SOURCE_DIR}/applications/petsc/vnv/gui/vnv.__registration__ 

