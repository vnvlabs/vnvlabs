#Little script to build everything and launch a server
#(the script is little -- this thing takes fooooorever to build)


cd env 
./docker.sh vnv_env:$1 
cd ..

cd vnv 
./docker.sh vnv_env:$1 vnv_raw:$1 
cd .. 

cd plugins 
./docker.sh vnv_raw:$1 vnv_base:$1 
cd .. 

cd gui 
./docker.sh vnv_base:$1 vnv_gui:$1  
cd ..

cd applications 
./docker.sh vnv_base:$1 $1 
cd .. 

#Build the dockerm image -- This is a flask server for managing docker containers. 
cd dockerm 
./docker.sh vnv_dockerm
cd ..


cd docker 
./docker.sh $1

