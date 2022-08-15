

REON=$1
REPO_OWNER=ghcr.io/vnvlabs
GITHASHNUM=$(git rev-parse --short HEAD)


#Inject the gui into everyone of the applications. 
#Do this now so we dont have to rebuild everything when we edit the gui.
for package in env demo proxy_apps mfem moose asgard all 
do
  
  docker build -t ${REPO_OWNER}/${package}:${REON} \
               --label vnvcommit="$GITHASHNUM" \
	       --build-arg FROM_IMAGE=vnv_${package}:latest \
	       --build-arg GUI_IMAGE=vnv_gui:latest . 

done

### Retag all the non vnv images . 
for package in dockerm serve 
do
  echo "FROM vnv_${package}:latest" | docker build --label vnvcommit="$GITHASHNUM" -t "${REPO_OWNER}/${package}:${REON}" -
done  



