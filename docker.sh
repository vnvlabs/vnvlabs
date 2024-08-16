
#!/bin/bash
set -e 
set -o pipefail

function check_and_build() {
    # Parameters
    REPO_NAME=$1
    BASE_IMAGE_NAME=$2
    DONE=$3

    # Get the current Git commit ID of the repository
    GIT_COMMIT_ID=$(cd $REPO_NAME && git rev-parse HEAD)
    BUILD_REPO=false

    # 1. Check if MODIFIED is false and perform actions
    if [ "$MODIFIED" = "no" ]; then
        docker pull ${REPO_OWNER}/${REPO_NAME}:${REON}
        CURRENT_COMMIT_ID=$(docker inspect --format='{{ index .Config.Labels "commit_id" }}' ${REPO_OWNER}/${REPO_NAME}:${REON} 2>/dev/null || echo "1")
        echo $GIT_COMMIT_ID
        echo $CURRENT_COMMIT_ID
        if [ "$CURRENT_COMMIT_ID" != "$GIT_COMMIT_ID" ]; then
            echo "Rebuilding as commit has changed"
            BUILD_REPO=true
        fi
    else
        BUILD_REPO=true
    fi

    # 2. Build and push the Docker image if needed
    if [ "$BUILD_REPO" = true ]; then
        MODIFIED="yes"
        docker build --label commit_id=$GIT_COMMIT_ID -f ${REPO_NAME}/vnv/Dockerfile -t ${REPO_OWNER}/${REPO_NAME}:${REON} --build-arg FROM_IMAGE=${REPO_OWNER}/${BASE_IMAGE_NAME}:${REON} $REPO_NAME
        docker push ${REPO_OWNER}/${REPO_NAME}:${REON}
    fi

    # If we are done with this image, then we can delete it
    if [ "$DONE" = "yes" ]; then
        docker rmi ${REPO_OWNER}/${REPO_NAME}:${REON}
	docker image prune -f 
    fi
}



REPO_OWNER=ghcr.io/vnvlabs
REON=run
MODIFIED="no"
LOWMEM="yes"

#Build the environment required to run all the applications
cd env 
docker pull ${REPO_OWNER}/env:${REON}
GIT_COMMIT_ID=$(sha256sum Dockerfile | cut -f1 -d' ')
CURRENT_COMMIT_ID=$(docker inspect --format='{{ index .Config.Labels "commit_id" }}' ${REPO_OWNER}/env:${REON} 2>/dev/null || echo "1")

echo $GIT_COMMIT_ID
echo $CURRENT_COMMIT_ID
if [ "$CURRENT_COMMIT_ID" != "$GIT_COMMIT_ID" ]; then
    docker build --label commit_id=$GIT_COMMIT_ID -f Dockerfile -t ${REPO_OWNER}/env:${REON} . 
    docker push ${REPO_OWNER}/env:${REON}
    MODIFIED="yes"
fi
cd ..

check_and_build "gui" "env" "no"
check_and_build "vnv" "gui" "no"

cd plugins
check_and_build "performance" "vnv" "no"
cd ..

cd applications
check_and_build "asgard" "performance" ${LOWMEM}
check_and_build "heat" "performance" ${LOWMEM}
check_and_build "simple" "performance" ${LOWMEM}
check_and_build "miniamr" "performance" ${LOWMEM}
check_and_build "swfft" "performance" ${LOWMEM}
check_and_build "hypre" "performance" "no"
check_and_build "petsc" "hypre" "no"
check_and_build "mfem" "petsc" ${LOWMEM}
check_and_build "libmesh" "petsc" "no"
check_and_build "moose" "libmesh" "yes"
