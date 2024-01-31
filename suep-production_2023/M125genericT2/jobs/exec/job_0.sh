#!/bin/sh

echo '----- START -----'
mkdir /tmp/VBFSUEP_2023/
cd /tmp/VBFSUEP_2023/
source /cvmfs/cms.cern.ch/cmsset_default.sh
export X509_USER_PROXY=/eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/proxy/x509up_u146772
export HOME=/afs/cern.ch/user/j/jkil

cd /eos/user/j/jkil/vbftrigger/suep-production_2023/CMSSW_13_0_14/src/
cmsenv
cd -
echo 'CMSSW_13_0_14 activated.'

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/gensim.py outputFile=file:gensim_0.root maxEvents=500 firstRun=0 seed=258167 &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/gensim_0.log
echo 'GENSIM created.'

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/digihlt.py inputFiles=file:gensim_0_numEvent500.root outputFile=file:digihlt_0.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/digihlt_0.log
echo 'DIGIHLT created.'
rm gensim_0_numEvent500.root

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/aod.py inputFiles=file:digihlt_0.root outputFile=file:aod_0.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/aod_0.log
echo 'AOD created.'
rm digihlt_0.root

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/miniaod.py inputFiles=file:aod_0.root outputFile=file:miniaod_0.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/miniaod_0.log
echo 'MINIAOD created.'
rm aod_0.root

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/nanoaod.py inputFiles=file:miniaod_0.root outputFile=file:nanoaod_0.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/nanoaod_0.log
echo 'NANOAOD created.'
rm miniaod_0.root
cp nanoaod_0.root /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/output/nanoaod
rm nanoaod_0.root
