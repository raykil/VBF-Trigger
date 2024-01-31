#!/bin/sh

echo '----- START -----'
mkdir /tmp/VBFSUEP_2023/
cd /tmp/VBFSUEP_2023/
source /cvmfs/cms.cern.ch/cmsset_default.sh
export X509_USER_PROXY=/eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/proxy/x509up_u146772
export HOME=/afs/cern.ch/user/j/jkil

cd /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/CMSSW_13_0_14/src/
cmsenv
cd -
echo 'CMSSW_13_0_14 activated.'

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/gensim.py outputFile=file:gensim_3.root maxEvents=500 firstRun=3 seed=543589 &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/gensim_3.log
echo 'GENSIM created.'

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/digihlt.py inputFiles=file:gensim_3_numEvent500.root outputFile=file:digihlt_3.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/digihlt_3.log
echo 'DIGIHLT created.'
rm gensim_3_numEvent500.root

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/aod.py inputFiles=file:digihlt_3.root outputFile=file:aod_3.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/aod_3.log
echo 'AOD created.'
rm digihlt_3.root

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/miniaod.py inputFiles=file:aod_3.root outputFile=file:miniaod_3.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/miniaod_3.log
echo 'MINIAOD created.'
rm aod_3.root

cmsRun /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/config_final/nanoaod.py inputFiles=file:miniaod_3.root outputFile=file:nanoaod_3.root &> /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/batchlogs/nanoaod_3.log
echo 'NANOAOD created.'
rm miniaod_3.root
cp nanoaod_3.root /eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/output/nanoaod
rm nanoaod_3.root
