

#Build asgard 
docker build -f asgard/docker/Dockerfile -t vnv_asgard:$2 --build-arg FROM_IMAGE=$1 asgard  &
asgard_pid=$!


#Build the heat
docker build -f heat/docker/Dockerfile -t vnv_heat:$2 --build-arg FROM_IMAGE=$1 heat &
heat_pid=$!

#Build simple 
docker build -f simple/docker/Dockerfile -t vnv_simple:$2--build-arg FROM_IMAGE=$1 simple &
simple_pid=$!

##miniamr
docker build -f miniamr/docker/Dockerfile -t vnv_miniamr:$2 --build-arg FROM_IMAGE=$1 miniamr &
miniamr_pid=$!

#swfft
docker build -f swfft/docker/Dockerfile -t vnv_swfft:$2 --build-arg FROM_IMAGE=$1 swfft &
swfft_pid=$!

#xsbench
docker build -f xsbench/docker/Dockerfile -t vnv_xs_bench:$2 --build-arg FROM_IMAGE=$1 xsbench &
xsbench_pid=$!

#hypre
docker build -f hypre/docker/Dockerfile -t vnv_hypre:$2 --build-arg FROM_IMAGE=$1 hypre
hypre_pid=$!

docker build -f petsc/docker/Dockerfile -t vnv_petsc:$2 --build-arg FROM_IMAGE=vnv_hypre:$2 petsc 

#mfem
docker build -f mfem/docker/Dockerfile -t vnv_mfem:$2 --build-arg FROM_IMAGE=vnv_petsc:$2 mfem &
mfem_pid=$!

#libmesh
docker build -f libmesh/docker/Dockerfile -t vnv_libmesh:$2 --build-arg FROM_IMAGE=vnv_petsc:$2 libmesh

#moose
docker build -f moose/docker/Dockerfile -t vnv_moose:$2 --build-arg FROM_IMAGE=vnv_libmesh:$2 moose 

wait 

#Demo App 
docker build -f docker/Dockerfile_demo -t vnv_demo:$2 --build-arg VERSION=$2 docker &

#Proxy Apps 
docker build -f docker/Dockerfile_proxyapps --build-arg VERSION=$2 -t vnv_proxy_apps:$2 docker &

#Kitchen Sink 
docker build -f docker/Dockerfile_all --build-arg VERSION=$2 -t vnv_all:$2 docker & 

wait 




