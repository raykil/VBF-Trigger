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

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/gensim.py outputFile=file:gensim_1.root maxEvents=500 firstRun=1 seed=619798 &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/gensim_1.log
echo 'GENSIM created.'

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/digihlt.py inputFiles=file:gensim_1_numEvent500.root outputFile=file:digihlt_1.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/digihlt_1.log
echo 'DIGIHLT created.'
rm gensim_1_numEvent500.root

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/aod.py inputFiles=file:digihlt_1.root outputFile=file:aod_1.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/aod_1.log
echo 'AOD created.'
rm digihlt_1.root

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/miniaod.py inputFiles=file:aod_1.root outputFile=file:miniaod_1.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/miniaod_1.log
echo 'MINIAOD created.'
rm aod_1.root

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/nanoaod.py inputFiles=file:miniaod_1.root outputFile=file:nanoaod_1.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/nanoaod_1.log
echo 'NANOAOD created.'
rm miniaod_1.root
cp nanoaod_1.root /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/output/nanoaod
rm nanoaod_1.root
