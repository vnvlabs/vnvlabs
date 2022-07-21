

REON=$1
REPO_OWNER=ghcr.io/vnvlabs
GITHASHNUM=$(git rev-parse --short HEAD)

./docker.sh

for package in env demo proxy_apps mfem moose asgard all dockerm  
do
  echo "FROM vnv_${package}:latest" | docker build --label vnvcommit="$GITHASHNUM" -t "${REPO_OWNER}/${package}:${REON}" -
  docker push ${REPO_OWNER}/${package}:${REON}
done



