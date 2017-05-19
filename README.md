# K-way-partitioning
Installation
____________

First of all you need to have cmake installed,

How to install cmake :
this is to install Homebrew, that will be used to install cmake

type in terminal:
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

then to install cmake:
brew install cmake

in order to run it you will need several metis downloaded and installed. Download it from there:
http://glaros.dtc.umn.edu/gkhome/metis/metis/download

then in the terminal select the folder and enter:
make config shared=1
make install
export METIS_DLL=/usr/local/lib/libmetis.dylib

for the next step you will need anaconda or similar, you can get it from there :

https://www.continuum.io/anaconda-overview


then go in the project folder and in terminal type :
conda env create -f environment.yml
