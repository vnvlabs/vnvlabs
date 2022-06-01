
docker build -f docker/Dockerfile -t vnv_serve_it --build-arg CONFIG_FILE=./docker/config.json .
docker run --network="host" -v /var/run/docker.sock:/var/run/docker.sock vnv_serve_it
