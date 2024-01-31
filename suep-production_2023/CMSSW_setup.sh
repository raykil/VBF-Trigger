#!/bin/bash

WORKDIR=$(dirname "$(readlink -f "$0")") # absolute path where CMSSW_setup.sh is located, which is suep-production_2023
echo -e '\nWorking directory: '$WORKDIR
source /cvmfs/cms.cern.ch/cmsset_default.sh

# Setting up CMSSW
RELEASE='CMSSW_13_0_14'
if [ ! -d "$WORKDIR/$RELEASE" ]; then
    echo -e '\nInitiating CMSSW setup...'
    cmsrel $RELEASE
    echo $RELEASE' installed.'
    cd $RELEASE/src/
    cmsenv
    git cms-addpkg PhysicsTools/NanoAOD
    echo -e '\nNanoAOD added to PhysicsTools.\n'
    git clone -b ul https://github.com/SUEPPhysics/SUEPNano.git PhysicsTools/SUEPNano
    echo -e '\nSUEPNano added to PhysicsTools.\n'
    cmsenv
    scram b -j 10
    cd ../../
else
    echo -e '\n'$RELEASE' is already installed. Skipping this step...'
fi

# Adding fragments to CMSSW
if [ -d "$WORKDIR/$RELEASE/src/PhysicsTools/SUEPNano/python/fragments" ]; then
    echo 'Deleting pre-existing fragments...'
    rm -r "$WORKDIR/$RELEASE/src/PhysicsTools/SUEPNano/python/fragments"
fi
echo -e '\nAdding fragments to CMSSW'
cp -r $WORKDIR'/fragments/' $WORKDIR'/'$RELEASE'/src/PhysicsTools/SUEPNano/python/'
cd $WORKDIR'/'$RELEASE'/src/'
scram b -j 12
cmsenv
echo 'Fragments successfully copied to '$RELEASE'/src/PhysicsTools/SUEPNano/python.'
cd $WORKDIR