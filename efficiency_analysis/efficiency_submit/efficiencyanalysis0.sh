#!/bin/sh

source ~/miniconda3/etc/profile.d/conda.sh
conda activate vbftrigger

python /eos/user/j/jkil/SUEP/vbftrigger/efficiency/EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetPtAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/LeadJetPtAnalysis.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency/EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubleadJetPtAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubleadJetPtAnalysis.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency/EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="MjjAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/MjjAnalysis.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency/EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="DetaAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/DetaAnalysis.log
 