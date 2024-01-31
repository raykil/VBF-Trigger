#!/bin/bash

# Make sure you are not in any conda environment.
cd CMSSW_13_0_14/src/
cmsenv
cd ../..

# Add other parameters as needed. For more details, see configSetup.py.
python3 configSetup.py --datatier=gensim
python3 configSetup.py --datatier=digihlt
python3 configSetup.py --datatier=aod
python3 configSetup.py --datatier=miniaod
python3 configSetup.py --datatier=nanoaod