
REPO_OWNER=ghcr.io/vnvlabs
REON=$1

set -e

#Build the environment required to run all the applications
cd env 
./docker.sh ${REPO_OWNER}/env:${REON} 
cd ..

#Build the vnv toolkit library
cd vnv 
./docker.sh ${REPO_OWNER}/env:${REON}  ${REPO_OWNER}/raw:${REON} 
cd .. 

#Add the gui to the image. This builds a heavy gui on top of the vnv image, and a light image
#on top of ubuntu:20.04
cd gui 
#./docker.sh <tag>
./docker.sh ${REPO_OWNER}/heavy_gui:${REON} ${REPO_OWNER}/raw:${REON} ${REPO_OWNER}/gui:${REON}
cd ..

#Add all of the plugins
cd plugins 
 ./docker.sh ${REPO_OWNER}/heavy_gui:${REON} ${REPO_OWNER}/base:${REON} 
cd .. 

#Build all of the applications. 
cd applications 
#./docker.sh <base image to build from> <repo name> <version>
./docker.sh ${REPO_OWNER}/base:${REON} ${REPO_OWNER} ${REON} 
cd .. 


if [[ x"${PUSH_TO_GHCR}" == "x1"  ]]; then

for package in env demo proxy_apps hypre petsc mfem moose asgard all gui   
do
  
  docker push ${REPO_OWNER}/${package}:${REON}
done

fi

