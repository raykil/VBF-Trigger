#!/bin/sh

source ~/miniconda3/etc/profile.d/conda.sh
conda activate vbftrigger

python /eos/user/j/jkil/SUEP/vbftrigger/efficiency/EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubLeadJetchEmEFAnalysis.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency/EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubLeadJetchHEFAnalysis.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency/EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubLeadJetneEmEFAnalysis.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency/EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubLeadJetneHEFAnalysis.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency/EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetmuEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/SubLeadJetmuEFAnalysis.log
