

REON=$1
REPO_OWNER=ghcr.io/vnvlabs
GITHASHNUM=$(git rev-parse --short HEAD)

./docker.sh ${REON}


for package in env demo proxy_apps hypre petsc mfem moose asgard all dockerm  
do
  docker push ${REPO_OWNER}/${package}:${REON}
done


