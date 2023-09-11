#!/bin/sh

source ~/miniconda3/etc/profile.d/conda.sh
conda activate vbftrigger

python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetPtAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/LeadJetPtAnalysis_tight.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubleadJetPtAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubleadJetPtAnalysis_tight.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="MjjAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/MjjAnalysis_tight.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="DetaAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/DetaAnalysis_tight.log
