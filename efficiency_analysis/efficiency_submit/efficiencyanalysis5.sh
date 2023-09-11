#!/bin/sh

source ~/miniconda3/etc/profile.d/conda.sh
conda activate vbftrigger

python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubLeadJetchEmEFAnalysis_tight.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubLeadJetchHEFAnalysis_tight.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubLeadJetneEmEFAnalysis_tight.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubLeadJetneHEFAnalysis_tight.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetmuEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubLeadJetmuEFAnalysis_tight.log
