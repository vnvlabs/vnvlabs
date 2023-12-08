


#Build MFEM
cd ${SOURCE_DIR}/applications/mfem \
    && rm -rf build \
    && mkdir -p build \
    && cd build \
    && cmake -DHYPRE_DIR=${HYPRE_DIR}\
             -DMETIS_DIR=${PETSC_DIR}\
             -DPETSC_DIR=${PETSC_DIR}\
             -DPETSC_ARCH=${PETSC_ARCH}\
             -DInjection_DIR=${VNV_DIR}/lib/cmake/\
             -DMFEM_USE_PETSC=ON\
             -DMFEM_USE_VNV=ON\
             -DCMAKE_EXPORT_COMPILE_COMMANDS=ON\
             -DBUILD_SHARED_LIBS=ON\
             -DCMAKE_INSTALL_PREFIX=${MFEM_DIR} .. \
    && make -j 8 \
    && make install \
    && ${VNV_REGISTER} gui mfem ${SOURCE_DIR}/applications/mfem/vnv/gui/vnv.__registration__ 



