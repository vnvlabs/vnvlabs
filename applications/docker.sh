#!/bin/bash
set -e 
set -o pipefail

REPO_OWNER=$2
REON=$3

#Build asgard 
docker build -f asgard/vnv/Dockerfile -t ${REPO_OWNER}/asgard:${REON} --build-arg FROM_IMAGE=$1 asgard  &

#Build the heat
docker build -f heat/vnv/Dockerfile -t ${REPO_OWNER}/heat:${REON} --build-arg FROM_IMAGE=$1 heat &

#Build simple 
docker build -f simple/vnv/Dockerfile -t ${REPO_OWNER}/simple:${REON} --build-arg FROM_IMAGE=$1 simple &

##miniamr
docker build -f miniamr/vnv/Dockerfile -t ${REPO_OWNER}/miniamr:${REON} --build-arg FROM_IMAGE=$1 miniamr &

#swfft
docker build -f swfft/vnv/Dockerfile -t ${REPO_OWNER}/swfft:${REON} --build-arg FROM_IMAGE=$1 swfft &

#hypre
docker build -f hypre/vnv/Dockerfile -t ${REPO_OWNER}/hypre:${REON} --build-arg FROM_IMAGE=$1 hypre

docker build -f petsc/vnv/Dockerfile -t ${REPO_OWNER}/petsc:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/hypre:${REON} petsc 

#mfem
docker build -f mfem/vnv/Dockerfile -t ${REPO_OWNER}/mfem:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/petsc:${REON} mfem &

#libmesh
docker build -f libmesh/vnv/Dockerfile -t ${REPO_OWNER}/libmesh:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/petsc:${REON} libmesh

#moose
docker build -f moose/vnv/Dockerfile -t ${REPO_OWNER}/moose:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/libmesh:${REON} moose 



wait 




