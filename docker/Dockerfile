ARG GUI_IMAGE=vnv_gui:latest
ARG FROM_IMAGE=vnv_demo:latest
FROM ${GUI_IMAGE} 

ARG FROM_IMAGE
FROM ${FROM_IMAGE}
COPY --from=0 /vnv-gui /vnv-gui
