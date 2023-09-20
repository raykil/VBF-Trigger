"""
    This program makes parquet files out of NANOAOD files.
    The parquet files include: OFFJets, HLTJets, MuonCollections, and TrigObjs.
    The command line looks like: "python makeobjects.py --rootpath={rootpath} --parqpath={parqpath} --dataset={dataset_name} --nparq={nparq}"
    * Caution! In {rootpath}, if the files are in DAS, leave it as default. If local, specify the absolute path of the directory.
    Raymond Kil, 2023
"""

from valid_def import MakeObjects
import awkward as ak
import numpy as np
import os
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")

parser.add_option("--rootpath", dest="rootpath", default="root://cms-xrd-global.cern.ch/", help="directory where the NANOAOD files are in.") # Ex) "/eos/user/j/jkil/SUEP/suep-production/2023_mu_NANOAOD/2023D_NANOAOD/"
parser.add_option("--parqpath", dest="parqpath", default="/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023D_parquets/" , help="directory where the created parquet files will be stored.")
parser.add_option("--dataset" , dest="dataset" , default="2023D_", help="prefix specifying the dataset. Now either 2023C_ or 2023D_")
parser.add_option("--nparq"   , dest="nparq"   , default=200, type=int, help="number of root files allocated to single parquet file")
parser.add_option("--beg"     , dest="beg"     , default=0, type=int, help="number of root files allocated to single parquet file")
parser.add_option("--fin"     , dest="fin"     , default=50, type=int, help="number of root files allocated to single parquet file")
(options, args) = parser.parse_args()

rootpath     = options.rootpath
parqpath     = options.parqpath
dataset_name = options.dataset
nparq        = options.nparq
beg          = options.beg
fin          = options.fin

if "cern.ch" in rootpath: # then it means root files are in DAS
    os.system("voms-proxy-init -voms cms -rfc")
    txtpath = input("Enter the path of the text file containing root file names: ")
    with open(txtpath, 'r') as t:
        rootfiles = [l.strip() for l in t.readlines()]
else:                     # root files are in local directory
    rootfiles = os.listdir(rootpath)
print(len(rootfiles))
#begs = [50, 100, 150, 200, 250, 300]
#fins = [100,150, 200, 250, 300, len(rootfiles)]
#fins = [200, 400, 600, 800, len(rootfiles)]
#begs = np.arange(0, len(rootfiles)//nparq*nparq+1, nparq, dtype=int)
#fins = np.append(np.arange(nparq, len(rootfiles), nparq, dtype=int),len(rootfiles))
begs = [beg]
fins = [fin]

for idx, beg in enumerate(begs):
    print(f"Starting {beg:04}-{fins[idx]-1:04}...")
    rootfile = rootfiles[beg:fins[idx]]
    OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections = MakeObjects(rootfile, rootpath)
    print(f"MakeObjects done for beg={beg:04}")

    ak.to_parquet(OFFJets,         f"{parqpath}{dataset_name}OFFJets{beg:04}-{fins[idx]-1:04}.parquet")
    ak.to_parquet(HLTJets,         f"{parqpath}{dataset_name}HLTJets{beg:04}-{fins[idx]-1:04}.parquet")
    ak.to_parquet(MuonCollections, f"{parqpath}{dataset_name}MuonCollections{beg:04}-{fins[idx]-1:04}.parquet")
    ak.to_parquet(TrigObjs,        f"{parqpath}{dataset_name}TrigObjs{beg:04}-{fins[idx]-1:04}.parquet")
    ak.to_parquet(METCollections,  f"{parqpath}{dataset_name}METCollections{beg:04}-{fins[idx]-1:04}.parquet")
    print(f"to_parquet done for beg={beg:04}")
