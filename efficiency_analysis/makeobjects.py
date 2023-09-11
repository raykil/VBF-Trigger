"""
    This program makes parquet files out of NANOAOD files.
    The parquet files include: OFFJets, HLTJets, MuonCollections, and TrigObjs.
    The command line looks like: "python new_makeobjects.py --rootpath={rootpath} --parqpath={parqpath} --dataset{dataset_name}"
    Raymond Kil, 2023
"""

from definitions import MakeObjects
import awkward as ak
import os
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")

parser.add_option("--rootpath", dest="rootpath", help="This is the directory where the NANOAOD files are in.") # Ex) "/eos/user/j/jkil/SUEP/suep-production/2023_mu_NANOAOD/2023D_NANOAOD/"
parser.add_option("--parqpath", dest="parqpath", help="This is the directory where the created parquet files will be stored.") # Ex) "/eos/user/j/jkil/SUEP/vbftrigger/efficiency/2023D_parquets/"
parser.add_option("--dataset" , dest="dataset" , help="This is the prefix specifying the dataset. Now either 2023C_ or 2023D_") # Ex) "2023D_"
(options, args) = parser.parse_args()

rootpath = options.rootpath
parqpath = options.parqpath
rootfiles = os.listdir(rootpath)
dataset_name = options.dataset

begs = [0  , 200, 400, 600, 800]
fins = [200, 400, 600, 800, len(rootfiles) ]
#begs = [800]
#fins = [len(rootfiles)]

for idx, beg in enumerate(begs):
    print(f"Starting {beg:04}-{fins[idx]-1:04}...")
    rootfile = rootfiles[beg:fins[idx]]
    OFFJets, HLTJets, MuonCollections, TrigObjs = MakeObjects(rootfile, rootpath)
    print(f"MakeObjects done for beg={beg:04}")

    ak.to_parquet(OFFJets,         f"{parqpath}{dataset_name}OFFJets{beg:04}-{fins[idx]-1:04}.parquet")
    ak.to_parquet(HLTJets,         f"{parqpath}{dataset_name}HLTJets{beg:04}-{fins[idx]-1:04}.parquet")
    ak.to_parquet(MuonCollections, f"{parqpath}{dataset_name}MuonCollections{beg:04}-{fins[idx]-1:04}.parquet")
    ak.to_parquet(TrigObjs,        f"{parqpath}{dataset_name}TrigObjs{beg:04}-{fins[idx]-1:04}.parquet")
    print(f"to_parquet done for beg={beg:04}")
