
#Build the performance plugin 
docker build -f performance/docker/Dockerfile -t $2 --build-arg FROM_IMAGE=$1 ./performance

#Dakota plugin not working yet!










