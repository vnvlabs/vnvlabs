



# mongo db is broken in apt -- install from source.
mkdir -p /temp_build
cd /temp_build  
git clone https://github.com/mongodb/mongo-c-driver.git \
    && cd mongo-c-driver \
    && git checkout 1.20.1 \
    && python3 build/calc_release_version.py > VERSION_CURRENT \
    && mkdir -p cmake-build \
    && cd cmake-build \
    && cmake -DENABLE_AUTOMATIC_INIT_AND_CLEANUP=OFF .. \
    && cmake --build . \
    && cmake --build . --target install
cd /temp_build && rm -r mongo-c-driver 

wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add - 
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
apt-get update && apt-get install -y mongodb-org
rm -r /temp_build
