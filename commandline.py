import subprocess

commands = [
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchEmEFAnalysis" --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchHEFAnalysis" --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneEmEFAnalysis" --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneHEFAnalysis" --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetmuEFAnalysis" --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',

    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchEmEFAnalysis" --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchHEFAnalysis" --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneEmEFAnalysis" --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneHEFAnalysis" --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetmuEFAnalysis" --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',

    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchEmEFAnalysis" --tightcuts=True --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetchHEFAnalysis" --tightcuts=True --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneEmEFAnalysis" --tightcuts=True --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetneHEFAnalysis" --tightcuts=True --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="LeadJetmuEFAnalysis" --tightcuts=True --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',

    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchEmEFAnalysis" --tightcuts=True --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetchHEFAnalysis" --tightcuts=True --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneEmEFAnalysis" --tightcuts=True --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetneHEFAnalysis" --tightcuts=True --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"',
    'python EfficiencyAnalysis.py --whichfiles="singlemuon" --triggerpath="pt105Analysis" --analysis="SubLeadJetmuEFAnalysis" --tightcuts=True --outputdir="/Users/raymondkil/Desktop/vbftrigger/effplot_newEF/"'
]

counter = 1
for command in commands:
    print("Starting the command {0}!".format(counter))
    subprocess.run(command, shell=True)
    print("command {0} done!".format(counter))
    counter += 1
    print("\n")