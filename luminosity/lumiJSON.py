"""
    This program retrieves the luminosity information from NANOAOD or MINIAOD files 
    and produces the JSON file in the format compatible to brilcalc.
    More information on brilcalc here: http://opendata.cern.ch/docs/cms-guide-luminosity-calculation#install-brilcalc.
    Raymond Kil, 2023 
"""

import uproot
import numpy as np
import awkward as ak
import os, json, glob, subprocess
from optparse import OptionParser

parser = OptionParser(usage="%prog [options]")
parser.add_option("--dataset"   , dest="dataset"   , default="root://cms-xrd-global.cern.ch/", help="possible entries: local dir to root files, datasets in DAS, luminosity parquet files. Globbing is allowed. Check readme.md for more detail.")
parser.add_option("--output"    , dest="output"    , default="./lumiJSON.txt"                , help="filepath for the output lumiJSON file")
parser.add_option("--goldenpath", dest="goldenpath", default="luminosity/2023golden.json"    , help="path of goldenJSON")
(options, args) = parser.parse_args()

dataset    = options.dataset.split(',')
output     = options.output
goldenpath = options.goldenpath

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def GetFileNames(dataset):
    datasets = sum([glob.glob(d) for d in dataset], [])
    filenames = []
    if 'dataset=' in datasets[0]: # DAS
        os.system("voms-proxy-init -voms cms -rfc")
        for d in dataset:
            runoutput = subprocess.run(["dasgoclient", "-query", f"file {d}"], capture_output=True, text=True)
            files = runoutput.stdout.strip().split('\n')
            filenames.extend(files)
    elif 'eos' in datasets[0]: # local dir
        for d in dataset:
            filenames.extend([d+f for f in os.listdir(d) if (".root" in f) or (".parq" in f)&("Lumi" in f)])
        if any("root" in f for f in filenames) and any("parq" in f for f in filenames):
            print("dangerous! Make sure that the directory does not contain both root files and parquet files.")
            sys.exit(1)
    return filenames

filenames = GetFileNames(dataset)
runs = {}
golden = json.load(open(goldenpath,'r'))

if "root" in filenames[0]: # root files
    for idx, filename in enumerate(filenames):
        if idx%100==0: print("processing ", filename[-41:])
        try:
            if "dataset=" in dataset[0]: path="root://cms-xrd-global.cern.ch//"
            with uproot.open(path + filename) as f:
                luminosities = f["LuminosityBlocks"]
                run, lum = luminosities["run"].array(), np.array(luminosities["luminosityBlock"].array(),dtype='int')
                for r,l in zip(run, lum):
                    r = str(r)
                    if r not in runs and r in golden.keys(): runs[r] = [l]
                    elif r in runs: runs[r].append(l)
                    else: pass
        except OSError as e:
            print(f"Failed to open {filename}. Moving on...")
            with open("open_failed.err", 'a') as err:
                err.write(f"Failed to open {filename}")

elif "parq" in filenames[0]: # parq files
    for filename in filenames:
        print("processing ", filename)
        luminosities = ak.from_parquet(filename)
        run, lum = luminosities.run, luminosities.lum
        for r,l in zip(run, lum):
            r = str(r)
            if r not in runs and r in golden.keys(): runs[r] = [l]
            elif r in runs: runs[r].append(l)
            else: pass

print("Lumi import done! Making it look GoLdeN...")

# expanding goldenJSON
expanded_golden = {}
for run in golden.keys():
    block = np.array([], dtype=int)
    for b in golden[run]:
        block = np.append(block, np.arange(b[0], b[1]+1))
    expanded_golden.update({run:list(block)})

# Cutting the events that are not golden
goldencut = []
for run in runs.keys():
    run = str(run)
    events_in_runs = ak.Array(runs[run])
    if run in expanded_golden.keys():
        goldencut = np.isin(events_in_runs,expanded_golden[run])
        runs[run] = events_in_runs[goldencut]
    else: del runs[run]

print("Looks GoLdeN! Moving on to organizing...")

# grouping lumis in bracket form [1,2,3,4,5,10] -> [[1,5],[10,10]]
for run in runs.keys():
    lumis = np.unique(runs[run])
    ranges = [[lumis[0], lumis[0]]]
    for l in lumis[1:]:
        if l == ranges[-1][1] + 1:
            ranges[-1][1] = l
        else:
            ranges.append([l, l])
    runs[run] = ranges

print("Organizing done! Saving...")

with open(output, 'w') as f: json.dump(runs, f, sort_keys=True, cls=NpEncoder)
print(f"Saving done! Output file here: {output}")