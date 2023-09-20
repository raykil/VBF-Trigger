"""
    This program retrieves the luminosity information from NANOAOD or MINIAOD files 
    and produces the JSON file in the format compatible to brilcalc.
    More information on brilcalc here: http://opendata.cern.ch/docs/cms-guide-luminosity-calculation#install-brilcalc.
    python lumiJSON.py --path={path} --output={output} --txtpath={txtpath}
    Raymond Kil, 2023
"""

# Things to improve
# get rid of lumiblocks outside goldenJSON

import uproot
import os
import json
import numpy as np
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")

parser.add_option("--path"   , dest="path" , default="root://cms-xrd-global.cern.ch/", help="local: directory where the aod files are. DAS: web server") # "/eos/user/j/jkil/SUEP/suep-production/2023_mu_NANOAOD/2023C_NANOAOD/"
parser.add_option("--output" , dest="output" , default="lumiJSON.txt")
parser.add_option("--txtpath" , dest="txtpath" , default="") # When fetching files from DAS, I need to provide the text file that contains file names.
parser.add_option("--goldenpath" , dest="goldenpath" , default="/eos/user/j/jkil/SUEP/vbftrigger/luminosity/2023golden.json", help="path of goldenJSON")
(options, args) = parser.parse_args()
path = options.path
output = options.output
txtpath = options.txtpath
goldenpath = options.goldenpath

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer) : return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray) : return obj.tolist()
        return super(NpEncoder, self).default(obj)

if "cms-xrd-global.cern.ch" in path:
    os.system("voms-proxy-init -voms cms -rfc")
    with open(txtpath, 'r') as t:
        filenames = [l.strip() for l in t.readlines()]
else:
    filenames = [f for f in os.listdir(path) if ".root" in f][:5]
    print("filenames", filenames)

runs = {}
golden = json.load(open(goldenpath,'r'))

for idx, filename in enumerate(filenames):
    if idx%100==0: print("processing ", filename[-41:])
    with uproot.open(path + filename) as f:
        luminosities = f["LuminosityBlocks"]
        run, lum = luminosities["run"].array(), np.array(luminosities["luminosityBlock"].array(),dtype='int')
        for r,l in zip(run, lum):
            r = str(r)
            if r not in runs and r in golden.keys(): runs[r] = [l]
            elif r in runs: runs[r].append(l)
            else: pass

print("Lumi import done! Making it look GoLdeN...")

for run in runs.keys():
    if run in golden.keys():
        gold_intervals, goldblocks = golden[run], []
        print("\nrun, runs[run]\n", run, "\n", runs[run])
        for gold in gold_intervals:
            i, f = gold
            goldblocks.extend(range(i, f+1))
        print("goldblocks\n", goldblocks)
        lumiblocks = runs[run]
        runs[run] = [l for l in lumiblocks if l in goldblocks]
    else: 
        print(f"run to be deleted (this shouldn't happen): {run}")

print("Looks GoLdeN! Moving on to organizing...")

for run in runs.keys():
    lumis = np.unique(runs[run])
    ranges = [[lumis[0], lumis[0]]]
    for l in lumis[1:]:
        if l == ranges[-1][1] + 1:
            ranges[-1][1] = l
        else:
            ranges.append([l, l])
    runs[run] = ranges

"""
for run in runs.keys():
    if run in golden.keys():
        lumi_intervals, gold_intervals = runs[run], golden[run]
        lumiblocks, goldblocks = [], []
        print("run", runs[run])
        for lumi in lumi_intervals:
            i, f = lumi
            lumiblocks.extend(range(i, f+1))
        print("lumiblocks", lumiblocks)
        for gold in gold_intervals:
            i, f = gold
            goldblocks.extend(range(i, f+1))
        print("goldblocks", goldblocks)

        for lumi, gold in lumi_intervals, gold_intervals:
            li, lf = lumi
            gi, gf = gold
            lumiblocks.extend(range(li, lf+1))
            goldblocks.extend(range(gi, gf+1))
            print("lumiblocks", lumiblocks)
            print("goldblocks", goldblocks)
    else:
        print(f"run to be deleted (this shouldn't happen): {run}")
"""

print("Organizing done! Saving...")

with open(output, 'w') as f: json.dump(runs, f, sort_keys=True, cls=NpEncoder)
print(f"Saving done! Output file here: {output}")