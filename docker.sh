
REPO_OWNER=ghcr.io/vnvlabs
REON=$1

set -e

#Build the environment required to run all the applications
cd env 
docker build -f Dockerfile -t ${REPO_OWNER}/env:${REON} . 
cd ..

#Build the vnv toolkit library
cd vnv 
docker build -f docker/Dockerfile --build-arg FROM_IMAGE=${REPO_OWNER}/env:${REON} -t ${REPO_OWNER}/raw:${REON} . 
cd .. 


#Build the gui top of ubuntu and on top of the vnv image. 

cd gui 
docker build -f docker/Dockerfile -t ${REPO_OWNER}/heavy_gui:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/raw:${REON} .
docker build -f docker/Dockerfile -t ${REPO_OWNER}/gui:${REON} .
cd ..

#Add all of the plugins
cd plugins 
 ./docker.sh ${REPO_OWNER}/heavy_gui:${REON} ${REPO_OWNER}/vnvlabs:${REON} 
cd .. 

#Build all of the applications. 
cd applications 
./docker.sh ${REPO_OWNER}/vnvlabs:${REON} ${REPO_OWNER} ${REON} 
cd .. 


if [[ x"${PUSH_TO_GHCR}" == "x1"  ]]; then

for package in env vnvlabs demo proxy_apps hypre petsc mfem moose asgard all gui   
do
  
  docker push ${REPO_OWNER}/${package}:${REON}
done

fi

