from ubuntu:20.04

ENV llvm_version=12
ENV TZ=America/New_York
ENV DEBIAN_FRONTEND=noninteractive 
ENV SOURCE_DIR=/vnvlabs
ENV SOFTWARE_DIR=/software
ENV ADIOS_DIR=${SOFTWARE_DIR}/adios
ENV LLVM_DIR=/usr/lib/llvm-${llvm_version}
ENV VNV_DIR=${SOFTWARE_DIR}/vnv
ENV VNV_MATCHER=${VNV_DIR}/bin/vnv-matcher
ENV VNV_REGISTER=${VNV_DIR}/bin/register 
ENV VNV_MERGE=${VNV_DIR}/bin/merge
ENV LD_LIBRARY_PATH=${VNV_DIR}/lib
ENV OPENMP_INCLUDE_DIR=/usr/lib/llvm-10/include/openmp
ENV Injection_DIR=${VNV_DIR}/lib/cmake
ENV THEIA_DEFAULT_PLUGINS=local-dir:/vnvgui/theia/plugins
ENV NODE_VERSION=18.0.0
ENV YARN_VERSION=1.22.19
ENV PARAVIEW_DIR=/vnvgui/paraview 
ENV PVPYTHON=${PARAVIEW_DIR}/bin/pvpython 
ENV PATH=/vnvgui/node/bin/:$PATH 
ENV HYPRE_DIR=${SOFTWARE_DIR}/hypre
ENV MFEM_DIR=${SOFTWARE_DIR}/mfem
ENV LIBMESH_DIR=${SOFTWARE_DIR}/libmesh 
ENV OMPI_ALLOW_RUN_AS_ROOT=1 
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 
ENV MOOSE_DIR=${SOURCE_DIR}/applications/moose
ENV PETSC_DIR=${SOFTWARE_DIR}/petsc
ENV PETSC_ARCH=""

COPY ./build_scripts/utils /build_scripts/utils


COPY ./build_scripts/build_apt_get.sh /build_scripts/build_apt_get.sh
RUN /build_scripts/build_apt_get.sh

COPY ./build_scripts/build_cmake.sh /build_scripts/build_cmake.sh
RUN /build_scripts/build_cmake.sh

COPY ./build_scripts/build_adios.sh /build_scripts/build_adios.sh
RUN /build_scripts/build_adios.sh

COPY ./build_scripts/build_papi.sh /build_scripts/build_papi.sh
RUN /build_scripts/build_papi.sh

COPY ./build_scripts/build_llvm.sh /build_scripts/build_llvm.sh
RUN /build_scripts/build_llvm.sh

COPY ./build_scripts/build_mongo.sh /build_scripts/build_mongo.sh
RUN /build_scripts/build_mongo.sh

COPY ./build_scripts/build_node.sh /build_scripts/build_node.sh
RUN /build_scripts/build_node.sh

COPY ./build_scripts/build_paraview.sh /build_scripts/build_paraview.sh
RUN /build_scripts/build_paraview.sh

COPY ./build_scripts/build_theia.sh /build_scripts/build_theia.sh
COPY ./gui/theia /vnvgui/theia
RUN /build_scripts/build_theia.sh

RUN apt-get -y purge openmpi-*

COPY /vnv ${SOURCE_DIR}/vnv
COPY ./build_scripts/build_vnv.sh /build_scripts/build_vnv.sh
RUN /build_scripts/build_vnv.sh

COPY /plugins/issues ${SOURCE_DIR}/plugins/issues
COPY ./build_scripts/build_issues.sh /build_scripts/build_issues.sh
RUN /build_scripts/build_issues.sh

COPY /plugins/performance ${SOURCE_DIR}/plugins/performance
COPY ./build_scripts/build_performance.sh /build_scripts/build_performance.sh
RUN /build_scripts/build_performance.sh

COPY /plugins/psip ${SOURCE_DIR}/plugins/psip
COPY ./build_scripts/build_psip.sh /build_scripts/build_psip.sh
RUN /build_scripts/build_psip.sh

COPY ./build_scripts/build_asgard.sh /build_scripts/build_asgard.sh
COPY ./applications/asgard ${SOURCE_DIR}/applications/asgard
RUN /build_scripts/build_asgard.sh

COPY ./build_scripts/build_simple.sh /build_scripts/build_simple.sh
COPY ./applications/simple ${SOURCE_DIR}/applications/simple
RUN /build_scripts/build_simple.sh

COPY ./build_scripts/build_heat.sh /build_scripts/build_heat.sh
COPY ./applications/heat ${SOURCE_DIR}/applications/heat
RUN /build_scripts/build_heat.sh

COPY ./build_scripts/build_miniamr.sh /build_scripts/build_miniamr.sh
COPY ./applications/miniamr ${SOURCE_DIR}/applications/miniamr
RUN /build_scripts/build_miniamr.sh

COPY ./build_scripts/build_swfft.sh /build_scripts/build_swfft.sh
COPY ./applications/swfft ${SOURCE_DIR}/applications/swfft
RUN /build_scripts/build_swfft.sh

COPY ./build_scripts/build_xsbench.sh /build_scripts/build_xsbench.sh
COPY ./applications/xsbench ${SOURCE_DIR}/applications/xsbench
RUN /build_scripts/build_xsbench.sh

COPY ./build_scripts/build_hypre.sh /build_scripts/build_hypre.sh
COPY ./applications/hypre ${SOURCE_DIR}/applications/hypre
RUN /build_scripts/build_hypre.sh

COPY ./build_scripts/build_petsc.sh /build_scripts/build_petsc.sh
COPY ./applications/petsc ${SOURCE_DIR}/applications/petsc
RUN /build_scripts/build_petsc.sh

COPY ./build_scripts/build_libmesh.sh /build_scripts/build_libmesh.sh
COPY ./applications/libmesh ${SOURCE_DIR}/applications/libmesh
RUN /build_scripts/build_libmesh.sh

COPY ./build_scripts/build_mfem.sh /build_scripts/build_mfem.sh
COPY ./applications/mfem ${SOURCE_DIR}/applications/mfem
RUN /build_scripts/build_mfem.sh


COPY ./build_scripts/build_moose.sh /build_scripts/build_moose.sh
COPY ./applications/moose ${SOURCE_DIR}/applications/moose
RUN /build_scripts/build_moose.sh

COPY ./build_scripts/build_gui.sh /build_scripts/build_gui.sh
COPY ./gui ${SOURCE_DIR}/gui
RUN /build_scripts/build_gui.sh

#Copy git stuff over and fix everything so it works
COPY .git ${SOURCE_DIR}/.git
COPY .gitmodules ${SOURCE_DIR}/.gitmodules
COPY ./build_scripts/build_git.sh /build_scripts/build_git.sh
RUN  /build_scripts/build_git.sh










