import subprocess

commands = [
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetPtAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubleadJetPtAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="MjjAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="DetaAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',

    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetmuEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',

    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetmuEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',

    # Tight cuts
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetPtAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubleadJetPtAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="MjjAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="DetaAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',

    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetmuEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',

    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneEmEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneHEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetmuEFAnalysis" --outputdir="/eos/user/j/jkil/www/VBFSUEP/efficiency/withJetLevelHLT/" --shape=True --tightcuts=True --datapath=/eos/user/j/jkil/SUEP/vbftrigger/efficiency/run3parqWjetinfo/'
]

counter = 1
for command in commands:
    print("Starting the command {0}!".format(counter))
    print(f"Starting the command")
    subprocess.run(command, shell=True)
    print("command {0} done!".format(counter))
    counter += 1
    print("\n")