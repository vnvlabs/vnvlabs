
#!/bin/bash
set -e 
set -o pipefail



REPO_OWNER=ghcr.io/vnvlabs
REON=run

#Build the environment required to run all the applications
cd env 
docker pull ${REPO_OWNER}/env:${REON} || echo "dne"
docker build -f Dockerfile -t ${REPO_OWNER}/env:${REON} . 
docker push ${REPO_OWNER}/env:${REON}
cd ..

#Build the gui top of ubuntu and on top of the vnv image. 

cd gui 
docker pull ${REPO_OWNER}/gui:${REON} || echo "dne"
docker build -f docker/Dockerfile -t ${REPO_OWNER}/gui:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/env:${REON} .
docker push ${REPO_OWNER}/gui:${REON}
cd ..

#Build the vnv toolkit library
cd vnv 
docker pull ${REPO_OWNER}/vnv:${REON} || echo "dne"
docker build -f docker/Dockerfile --build-arg FROM_IMAGE=${REPO_OWNER}/gui:${REON} -t ${REPO_OWNER}/vnv:${REON} . 
docker push ${REPO_OWNER}/vnv:${REON}
cd .. 

#Add all of the plugins
cd plugins/performance
docker pull ${REPO_OWNER}/vnvp:${REON} || echo "dne"
docker build -f docker/Dockerfile --build-arg FROM_IMAGE=${REPO_OWNER}/vnv:${REON} -t ${REPO_OWNER}/vnvp:${REON} .  
docker push ${REPO_OWNER}/vnvp:${REON}
cd ../.. 


#Build all of the applications. 
cd applications 
./docker.sh ${REPO_OWNER}/vnvp:${REON} ${REPO_OWNER} ${REON} 
cd .. 



