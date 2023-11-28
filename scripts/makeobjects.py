"""
    This program makes parquet files out of NANOAOD files.
    The parquet files include: OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections, and Luminosities.
    The command line looks like: "python makeobjects.py --rootpath={rootpath} --parqpath={parqpath} --dataset={dataset_name} --nparq={nparq}"
    Raymond Kil, 2023
"""

import numpy as np
import awkward as ak
import definitions as vbf
from optparse import OptionParser

parser = OptionParser(usage="%prog [options]")
parser.add_option('--filenames', dest='filenames', default='', help='path to the .txt file that contains the list of nanoaod file names.')
parser.add_option('--parqpath', dest='parqpath', default="./"  , help='directory where the created parquet files will be stored.')
parser.add_option('--dataset', dest='dataset', default='', help="path to the directory where the produced parquet files will be placed")
parser.add_option('--nparq', dest='nparq', default=200, type=int, help='Maximum number of nanoaod files to be included in one parquet file')
parser.add_option('--onlymake', dest='onlymake', default='')
(options, args) = parser.parse_args()

filenames = options.filenames
parqpath  = options.parqpath
dataset   = options.dataset
nparq     = options.nparq
onlymake  = options.onlymake

print(f"Staring makeobjects for dataset {dataset}")

with open(filenames,'r') as f: 
    rootfiles = [root.strip('\n') for root in f.readlines()]

begs = np.arange(0, len(rootfiles)//nparq*nparq+1, nparq, dtype=int)
fins = np.append(np.arange(nparq, len(rootfiles)+1, nparq, dtype=int),len(rootfiles))

if "store" in rootfiles[0]: # DAS
    prefix = "root://cms-xrd-global.cern.ch//"
elif "eos" in rootfiles[0]: # local directory
    prefix = ""

for beg, fin in zip(begs, fins):
    print(f"Starting {beg:04}-{fin-1:04}...")
    rootfile = [f"{prefix}{root}" for root in rootfiles[beg:fin]]
    OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections, Luminosities = vbf.MakeObjects(rootfile)
    print(f"MakeObjects done for nanoaod files {beg:04}-{fin-1:04}")

    ak.to_parquet(OFFJets,         f"{parqpath}{dataset}_OFFJets{beg:04}-{fin-1:04}.parquet")
    ak.to_parquet(HLTJets,         f"{parqpath}{dataset}_HLTJets{beg:04}-{fin-1:04}.parquet")
    ak.to_parquet(MuonCollections, f"{parqpath}{dataset}_MuonCollections{beg:04}-{fin-1:04}.parquet")
    ak.to_parquet(TrigObjs,        f"{parqpath}{dataset}_TrigObjs{beg:04}-{fin-1:04}.parquet")
    ak.to_parquet(METCollections,  f"{parqpath}{dataset}_METCollections{beg:04}-{fin-1:04}.parquet")
    ak.to_parquet(Luminosities,    f"{parqpath}{dataset}_Luminosities{beg:04}-{fin-1:04}.parquet")
    print(f"Parquet files made: {parqpath}{dataset}_*{beg:04}-{fin-1:04}.parquet")