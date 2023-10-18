"""
    This program retrieves the luminosity information from NANOAOD or MINIAOD files 
    and produces the JSON file in the format compatible to brilcalc.
    More information on brilcalc here: http://opendata.cern.ch/docs/cms-guide-luminosity-calculation#install-brilcalc.
    Raymond Kil, 2023 
"""

import uproot
import awkward as ak
import os
import json
import numpy as np

path = "/eos/user/j/jkil/SUEP/suep-production/2023_mu_NANOAOD/2023C_NANOAOD/"
filenames = os.listdir(path)
runs = {}

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

for idx, filename in enumerate(filenames):
    if idx%100==0: print("processing ", filename)
    with uproot.open(path + filename) as f:
        luminosities = f["LuminosityBlocks"]
        run, lum = luminosities["run"].array(), np.array(luminosities["luminosityBlock"].array(),dtype='int')
        if ak.all(run==run[0]): 
            key = str(run[0])
            if key in runs: 
                runs[key] = np.append(runs[key], lum)
            else: 
                runs[key] = lum
        else:
            print(f"Run values are inhomogeneous in file {filename}. Take care of it!")

print("lumi import done! Moving on to organizing...")

for key in runs.keys():
    lumis = runs[key]
    lumis = np.unique(lumis)
    #print(f"keys: {key}, \nlumis: {lumis}")
    ranges = [[lumis[0], lumis[0]]]
    for l in lumis[1:]:
        if l == ranges[-1][1] + 1:
            ranges[-1][1] = l
        else:
            ranges.append([l, l])
    runs[key] = ranges

print("Organizing done! Saving...")

with open("lumiJSON.txt", 'w') as f: json.dump(runs, f, sort_keys=True, cls=NpEncoder)
print(f"Saving done!")