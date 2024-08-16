#!/bin/bash
set -e 
set -o pipefail

REPO_OWNER=$2
REON=$3

#Build asgard 

docker pull ${REPO_OWNER}/asgard:${REON} || echo "dne"
docker build -f asgard/vnv/Dockerfile -t ${REPO_OWNER}/asgard:${REON} --build-arg FROM_IMAGE=$1 asgard 
docker push ${REPO_OWNER}/asgard:${REON}

#Build the heat

docker pull ${REPO_OWNER}/heat:${REON} || echo "dne"
docker build -f heat/vnv/Dockerfile -t ${REPO_OWNER}/heat:${REON} --build-arg FROM_IMAGE=$1 heat 
docker push ${REPO_OWNER}/heat:${REON}
#Build simple 

docker pull ${REPO_OWNER}/simple:${REON} || echo "dne"
docker build -f simple/vnv/Dockerfile -t ${REPO_OWNER}/simple:${REON} --build-arg FROM_IMAGE=$1 simple 
docker push ${REPO_OWNER}/simple:${REON}
##miniamr

docker pull ${REPO_OWNER}/miniamr:${REON} || echo "dne"
docker build -f miniamr/vnv/Dockerfile -t ${REPO_OWNER}/miniamr:${REON} --build-arg FROM_IMAGE=$1 miniamr 
docker push ${REPO_OWNER}/miniamr:${REON}
#swfft

docker pull ${REPO_OWNER}/swfft:${REON} || echo "dne"
docker build -f swfft/vnv/Dockerfile -t ${REPO_OWNER}/swfft:${REON} --build-arg FROM_IMAGE=$1 swfft
docker push ${REPO_OWNER}/swfft:${REON}
#hypre

docker pull ${REPO_OWNER}/hypre:${REON} || echo "dne"
docker build -f hypre/vnv/Dockerfile -t ${REPO_OWNER}/hypre:${REON} --build-arg FROM_IMAGE=$1 hypre
docker push ${REPO_OWNER}/hypre:${REON}

docker pull ${REPO_OWNER}/petsc:${REON} || echo "dne"
docker build -f petsc/vnv/Dockerfile -t ${REPO_OWNER}/petsc:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/hypre:${REON} petsc 
docker push ${REPO_OWNER}/petsc:${REON}
#mfem

docker pull ${REPO_OWNER}/mfem:${REON} || echo "dne"
docker build -f mfem/vnv/Dockerfile -t ${REPO_OWNER}/mfem:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/petsc:${REON} mfem 
docker push ${REPO_OWNER}/mfem:${REON}
#libmesh

docker pull ${REPO_OWNER}/libmesh:${REON} || echo "dne"
docker build -f libmesh/vnv/Dockerfile -t ${REPO_OWNER}/libmesh:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/petsc:${REON} libmesh
docker push ${REPO_OWNER}/libmesh:${REON}
#moose

docker pull ${REPO_OWNER}/moose:${REON} || echo "dne"
docker build -f moose/vnv/Dockerfile -t ${REPO_OWNER}/moose:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/libmesh:${REON} moose 
docker push ${REPO_OWNER}/moose:${REON}






