import subprocess

commands = [
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetPtAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubleadJetPtAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="MjjAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="DetaAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',

    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchEmEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchHEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneEmEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneHEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetmuEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',

    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchEmEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchHEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneEmEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneHEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetmuEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True',

    # Tight cuts
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetPtAnalysis" --outputdir="./jetlevel_effplots/" --shape=True  --tightcuts=True',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubleadJetPtAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="MjjAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',
    'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="DetaAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',

    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchEmEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchHEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneEmEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneHEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetmuEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',

    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchEmEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchHEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneEmEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneHEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True',
    #'python efficiencyanalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetmuEFAnalysis" --outputdir="./jetlevel_effplots/" --shape=True --tightcuts=True'
]

counter = 1
for command in commands:
    print("Starting the command {0}!".format(counter))
    print(f"Starting the command")
    subprocess.run(command, shell=True)
    print("command {0} done!".format(counter))
    counter += 1
    print("\n")