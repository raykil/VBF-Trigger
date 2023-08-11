from definitions import MakeObjects
import awkward as ak
import os

rootpath = "/eos/user/j/jkil/SUEP/suep-production/2023C_mu_NANOAOD_withJetFB/NANOAOD/"
parqpath = "/eos/user/j/jkil/SUEP/vbftrigger/run3parqWjetinfo/"
rootfiles = os.listdir(rootpath)

begs = [0  ,200,400,600,800 ,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000,5200]
fins = [200,400,600,800,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000,5200, -1 ]

for idx, beg in enumerate(begs):
    print(f"Starting {beg}-{fins[idx]-1}...")
    rootfile = rootfiles[beg:fins[idx]]
    OFFJets, HLTJets, MuonCollections, TrigObjs = MakeObjects(rootfile, rootpath)
    print(f"MakeObjects done for beg={beg}")

    ak.to_parquet(OFFJets, f"{parqpath}OFFJets{beg}-{fins[idx]-1}.parquet")
    ak.to_parquet(HLTJets, f"{parqpath}HLTJets{beg}-{fins[idx]-1}.parquet")
    ak.to_parquet(MuonCollections, f"{parqpath}MuonCollections{beg}-{fins[idx]-1}.parquet")
    ak.to_parquet(TrigObjs, f"{parqpath}TrigObjs{beg}-{fins[idx]-1}.parquet")
    print(f"to_parquet done for beg={beg}")