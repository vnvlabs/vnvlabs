ARG GUI_IMAGE=vnv_gui:latest
FROM ${GUI_IMAGE} as GUI


ARG FROM_IMAGE=vnv_demo
FROM ${FROM_IMAGE}:latest
LABEL vnvcommit=""
COPY --fromi=GUI /vnv-gui /vnv-gui
