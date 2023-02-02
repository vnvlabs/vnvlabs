

REPO_OWNER=$2
REON=$3

#Build asgard 
docker build -f asgard/docker/Dockerfile -t ${REPO_OWNER}/asgard:${REON} --build-arg FROM_IMAGE=$1 asgard  &

#Build the heat
docker build -f heat/docker/Dockerfile -t ${REPO_OWNER}/heat:${REON} --build-arg FROM_IMAGE=$1 heat &

#Build simple 
docker build -f simple/docker/Dockerfile -t ${REPO_OWNER}/simple:${REON} --build-arg FROM_IMAGE=$1 simple &

##miniamr
docker build -f miniamr/docker/Dockerfile -t ${REPO_OWNER}/miniamr:${REON} --build-arg FROM_IMAGE=$1 miniamr &

#swfft
docker build -f swfft/docker/Dockerfile -t ${REPO_OWNER}/swfft:${REON} --build-arg FROM_IMAGE=$1 swfft &

#xsbench
docker build -f xsbench/docker/Dockerfile -t ${REPO_OWNER}/xsbench:${REON} --build-arg FROM_IMAGE=$1 xsbench &

#hypre
docker build -f hypre/docker/Dockerfile -t ${REPO_OWNER}/hypre:${REON} --build-arg FROM_IMAGE=$1 hypre

docker build -f petsc/docker/Dockerfile -t ${REPO_OWNER}/petsc:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/hypre:${REON} petsc 

#mfem
docker build -f mfem/docker/Dockerfile -t ${REPO_OWNER}/mfem:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/petsc:${REON} mfem &
mfem_pid=$!

#libmesh
docker build -f libmesh/docker/Dockerfile -t ${REPO_OWNER}/libmesh:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/petsc:${REON} libmesh

#moose
docker build -f moose/docker/Dockerfile -t ${REPO_OWNER}/moose:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/libmesh:${REON} moose 

wait 

#Demo App 
docker build -f docker/Dockerfile_demo -t ${REPO_OWNER}/demo:${REON} --build-arg VERSION=${REON} --build-arg REPO=${REPO_OWNER} docker &

#Proxy Apps 
docker build -f docker/Dockerfile_proxyapps -t  ${REPO_OWNER}/proxy_apps:${REON} --build-arg VERSION=${REON} --build-arg REPO=${REPO_OWNER} docker &

#Kitchen Sink 
docker build -f docker/Dockerfile_all -t ${REPO_OWNER}/all:${REON} --build-arg VERSION=${REON} --build-arg REPO=${REPO_OWNER} docker & 

wait 




