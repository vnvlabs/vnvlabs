
REPO_OWNER=$1
REON=$2


cd env 
#./docker.sh <tag>
./docker.sh ${REPO_OWNER}/env:${REON} 
cd ..

cd vnv 
#./docker.sh <base image to build from> <tag>
./docker.sh ${REPO_OWNER}/env:${REON}  ${REPO_OWNER}/raw:${REON} 
cd .. 


cd plugins 

#./docker.sh <base image to build from> <tag>
 ./docker.sh ${REPO_OWNER}/raw:${REON} ${REPO_OWNER}/base:${REON} 
cd .. 

cd applications 
#./docker.sh <base image to build from> <repo name> <version>
./docker.sh ${REPO_OWNER}/base:${REON} ${REPO_OWNER} ${REON} 
cd .. 

cd gui 
#./docker.sh <tag>
./docker.sh ${REPO_OWNER}/gui:${REON}  
cd ..

cd dockerm 
# ./docker.sh <tag> <image to use when appending gui to containers>
./docker.sh ${REPO_OWNER}/dockerm:${REON} ${REPO_OWNER}/gui:${REON}  
cd ..

if [[ x"${PUSH_TO_GHCR}" == "x1"  ]]; then

for package in env demo proxy_apps hypre petsc mfem moose asgard all dockerm gui   
do
  docker push ${REPO_OWNER}/${package}:${REON}
done

fi

