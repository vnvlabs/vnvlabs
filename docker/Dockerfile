
ARG FROM_IMAGE=ghcr.io/vnvlabs/serve:latest
FROM ${FROM_IMAGE}


ARG CONFIG_FILE=config.json 
COPY ${CONFIG_FILE} /conf/config.json

WORKDIR /serve
ENTRYPOINT ["virt/bin/python3", "src/run.py", "/conf/config.json"]
