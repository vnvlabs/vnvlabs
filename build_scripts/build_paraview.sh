


#Install Pavaview server (used for visualization) 
mkdir -p /vnvgui/paraview
cd /vnvgui
wget -O pv.tar.gz "https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.10&type=binary&os=Linux&downloadFile=ParaView-5.10.1-osmesa-MPI-Linux-Python3.9-x86_64.tar.gz"
tar -xf /vnvgui/pv.tar.gz -C /vnvgui/paraview --strip-components=1 && rm /vnvgui/pv.tar.gz 

