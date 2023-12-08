


#Install LIBMESH VNV
cd ${SOURCE_DIR}/applications/libmesh \
     && ./configure --with-methods="opt"\
                    --with-mpi-lib=/usr/lib/x86_64-linux-gnu/\
                    --with-mpi-include=/usr/include/x86_64-linux-gnu/mpich\
                    --prefix=${LIBMESH_DIR} \
                    --enable-silent-rules \
                    --enable-unique-id \
                    --disable-warnings \
                    --with-thread-model=openmp\
                    --with-vnv=${VNV_DIR}\
                    --with-metis=PETSc\
                    --with-parmetis=PETSc\
                    --disable-maintainer-mode\
                    --enable-petsc-hypre-required \
    && bear make -j \
    && ${VNV_MATCHER} --package LIBMESH \
                      --output src/utils/vnv_LIBMESH.C \
                      --fix-omp \
		              --ignore-dir ./contrib \
                      --cache src/utils/vnv.__cache__\
                      compile_commands.json\
    && make -j \
    && make install\
    && ${VNV_REGISTER} gui libmesh ${SOURCE_DIR}/applications/libmesh/vnv/gui/vnv.__registration__
