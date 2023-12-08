

#Build the moose hit bindings
cd ${SOURCE_DIR}/gui/app/moose/pyhit/hitsrc && make hit bindings 


cd ${SOURCE_DIR}/gui
virtualenv virt
virt/bin/pip install -r requirements.txt 

