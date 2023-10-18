"""
    This sh files are for efficiency analysis
"""

import os
"""
path = "/eos/user/j/jkil/SUEP/vbftrigger/datasets/parq/"
analyses = ["mjj", "deta", "met"]
goldenpath = "/eos/user/j/jkil/SUEP/vbftrigger/luminosity/2023golden.json"
outputdir = "/afs/cern.ch/user/j/jkil/efficiencyanalysis/exec/"

datasets = [dset[:-5] for dset in os.listdir(path) if "fb" not in dset]
for dset in datasets:
    jsondir = f"/eos/user/j/jkil/SUEP/vbftrigger/datasets/json/{dset}_json/"
    for analysis in analyses:
        with open(f"{outputdir}{dset}_{analysis}.sh", 'w') as sh:
            sh.write("#!/bin/sh\n")
            sh.write("\n")
            sh.write("source ~/miniconda3/etc/profile.d/conda.sh\n")
            sh.write("conda activate vbftrigger\n")
            sh.write("\n")
            if "C" in dset: triggerpaths = ["pt75", "pt110"]
            elif "D" in dset:triggerpaths = ["pt80", "pt110"]
            for triggerpath in triggerpaths:
                sh.write(f"python /eos/user/j/jkil/SUEP/vbftrigger/scripts/efficiencyanalysis.py --triggerpath={triggerpath} --analysis={analysis} --tightcuts=tight --goldenpath={goldenpath} --dataset={dset} --outputdir={jsondir} > /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/{dset}_{triggerpath}_{analysis}.log\n")
"""
analyses = ["leadpt", "mjj", "deta"]
datasets  = ["promC0v3fb", "promC1v3fb", "promC01v4fb", "promD0v1fb", "promD1v1fb", "promD01v2fb"]
for dataset in datasets:
    for analysis in analyses:
        with open(f"/afs/cern.ch/user/j/jkil/efficiencyanalysis/exec/{dataset}_{analysis}.sh", 'w') as sh:
            sh.write("#!/bin/sh\n")
            sh.write("\n")
            sh.write("source ~/miniconda3/etc/profile.d/conda.sh\n")
            sh.write("conda activate vbftrigger\n")
            sh.write("\n")
            sh.write(f"python /eos/user/j/jkil/SUEP/vbftrigger/scripts/efficiencyanalysis.py --triggerpath=pt105 --analysis={analysis} --tightcuts=tight --filterbits=True --goldenpath=/eos/user/j/jkil/SUEP/vbftrigger/luminosity/2023golden.json --dataset={dataset} --outputdir=/eos/user/j/jkil/SUEP/vbftrigger/datasets/json/{dataset}_json/ > /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/{dataset}_{analysis}_pt105_tight.log\n")
            sh.write(f"python /eos/user/j/jkil/SUEP/vbftrigger/scripts/efficiencyanalysis.py --triggerpath=pt105 --analysis={analysis} --filterbits=True --goldenpath=/eos/user/j/jkil/SUEP/vbftrigger/luminosity/2023golden.json --dataset={dataset} --outputdir=/eos/user/j/jkil/SUEP/vbftrigger/datasets/json/{dataset}_json/ > /afs/cern.ch/user/j/jkil/efficiencyanalysis/batchlogs/{dataset}_{analysis}_pt105.log")