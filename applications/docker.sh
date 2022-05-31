

#Build asgard 
docker build -f asgard/docker/Dockerfile -t vnv_asgard --build-arg FROM_IMAGE=$1 asgard  &
asgard_pid=$!


#Build the heat
docker build -f heat/docker/Dockerfile -t vnv_heat --build-arg FROM_IMAGE=$1 heat &
heat_pid=$!

#Build simple 
docker build -f simple/docker/Dockerfile -t vnv_simple --build-arg FROM_IMAGE=$1 simple &
simple_pid=$!

#miniamr
docker build -f miniamr/docker/Dockerfile -t vnv_miniamr --build-arg FROM_IMAGE=$1 miniamr &
miniamr_pid=$!

#swfft
docker build -f swfft/docker/Dockerfile -t vnv_swfft --build-arg FROM_IMAGE=$1 swfft &
swfft_pid=$!

#xsbench
docker build -f xsbench/docker/Dockerfile -t vnv_xs_bench --build-arg FROM_IMAGE=$1 xsbench &
xsbench_pid=$!

#hypre
docker build -f hypre/docker/Dockerfile -t vnv_hypre --build-arg FROM_IMAGE=$1 hypre
hypre_pid=$!

docker build -f petsc/docker/Dockerfile -t vnv_petsc --build-arg FROM_IMAGE=vnv_hypre petsc 

#mfem
docker build -f mfem/docker/Dockerfile -t vnv_mfem --build-arg FROM_IMAGE=vnv_petsc mfem &
mfem_pid=$!

#libmesh
docker build -f libmesh/docker/Dockerfile -t vnv_libmesh --build-arg FROM_IMAGE=vnv_petsc libmesh

#moose
docker build -f moose/docker/Dockerfile -t vnv_moose --build-arg FROM_IMAGE=vnv_libmesh moose 

wait 

#Demo App 
docker build -f docker/Dockerfile_demo -t vnv_demo docker &

#Proxy Apps 
docker build -f docker/Dockerfile_proxyapps -t vnv_proxy_apps docker &

#Kitchen Sink 
docker build -f docker/Dockerfile_all -t vnv_all docker & 

wait 




