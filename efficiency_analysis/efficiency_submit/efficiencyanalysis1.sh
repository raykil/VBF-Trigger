#!/bin/sh

source ~/miniconda3/etc/profile.d/conda.sh
conda activate vbftrigger

python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/LeadJetchEmEFAnalysis.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/LeadJetchHEFAnalysis.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/LeadJetneEmEFAnalysis.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/LeadJetneHEFAnalysis.log
python /eos/user/j/jkil/SUEP/vbftrigger/efficiency_analysis/efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetmuEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023CD_parquets/ &> /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/LeadJetmuEFAnalysis.log
