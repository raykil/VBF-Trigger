import definitions as vbf
import numpy as np
from optparse import OptionParser
import os
import awkward as ak
parser = OptionParser(usage="%prog [options]")

parser.add_option("--dataset" , dest="dataset" , default="", help="prefix specifying the dataset. Ex) C0v3_")
(options, args) = parser.parse_args()
dataset = options.dataset

path = "/eos/user/j/jkil/SUEP/vbftrigger/datasets/parq/"
destpath = "/eos/user/j/jkil/SUEP/vbftrigger/datasets/new_parq/"
daspath = "root://cms-xrd-global.cern.ch//"
if not os.path.exists(f"{destpath}{dataset}"): os.system(f"mkdir {destpath}{dataset}")

nparq = 200
print("starting...")
with open(f"{path}{dataset}/filenames.txt", 'r') as f:
    rootfiles = [l[:-1] for l in f.readlines()]
    begs = np.arange(0, len(rootfiles)//nparq*nparq+1, nparq, dtype=int)
    fins = np.append(np.arange(nparq, len(rootfiles)+1, nparq, dtype=int),len(rootfiles))
    for beg, fin in zip(begs, fins):
        rootfile = rootfiles[beg:fin]
        OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections, Luminosities = vbf.MakeObjects(rootfile, daspath)
        ak.to_parquet(OFFJets,         f"{destpath}{dataset}/{dataset[4:]}OFFJets{beg:04}-{fin-1:04}.parquet")
        ak.to_parquet(HLTJets,         f"{destpath}{dataset}/{dataset[4:]}HLTJets{beg:04}-{fin-1:04}.parquet")
        ak.to_parquet(MuonCollections, f"{destpath}{dataset}/{dataset[4:]}MuonCollections{beg:04}-{fin-1:04}.parquet")
        ak.to_parquet(TrigObjs,        f"{destpath}{dataset}/{dataset[4:]}TrigObjs{beg:04}-{fin-1:04}.parquet")
        ak.to_parquet(METCollections,  f"{destpath}{dataset}/{dataset[4:]}METCollections{beg:04}-{fin-1:04}.parquet")
        ak.to_parquet(Luminosities,    f"{destpath}{dataset}/{dataset[4:]}Luminosities{beg:04}-{fin-1:04}.parquet")