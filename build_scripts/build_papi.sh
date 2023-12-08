


mkdir -p /temp_build
cd /temp_build
git clone https://github.com/icl-utk-edu/papi.git &&  cd papi/src && ./configure && make && make install  
cd /temp_build 
rm -r /temp_build


