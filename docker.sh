#Little script to build everything and launch a server
#(the script is little -- this thing takes fooooorever to build)


#cd env 
#./docker.sh vnv_env 
#cd ..

cd vnv 
./docker.sh vnv_env vnv_raw 
cd .. 

cd plugins 
./docker.sh vnv_raw vnv_base 
cd .. 

cd gui 
./docker.sh vnv_base vnv_gui 
cd ..

cd applications 
./docker.sh vnv_gui vnv_gui
cd .. 

cd server
./docker.sh vnv_env vnv_serve
cd ..

#Build the dockerm image -- This is a flask server for managing docker containers. 
cd dockerm 
./docker.sh vnv_dockerm
cd ..

cd saas
./docker.sh vnv_saas


