

REON=$1
REPO_OWNER=ghcr.io/vnvlabs


for package in env demo proxy_apps mfem moose asgard all serve 
do
docker tag vnv_${package}:latest ${REPO_OWNER}/${package}:${REON}
docker push ${REPO_OWNER}/${package}:${REON}
done



