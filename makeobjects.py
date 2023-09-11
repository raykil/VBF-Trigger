import definitions as vbf
import awkward as ak

#txtfiles = ["Mu0_2023C.txt", "Mu1_2023C.txt"]
txtfiles = ["Mu1_2023C.txt"]
#path = "root://cms-xrd-global.cern.ch/"
path = "root://cmsxrootd.fnal.gov/"
begs = [0  , 20, 40, 60, 80 , 100, 120, 140]
fins = [20 , 40, 60, 80, 100, 120, 140, -1 ]
nums = ["0","1","2","3", "4", "5", "6", "7"]

filenames0, filenames1 = [], []
#filenames = [filenames0, filenames1]
filenames = [filenames1]
# After _TrigObjs0 and _TrigObjs1 are made with Mu1, then I move on to produce rest of them (from 2).

for t, txtfile in enumerate(txtfiles):
    with open(txtfile, 'r') as r:
        for line in r:
            filenames[t].append(line.strip())

for f, filename in enumerate(filenames):
    print("starting ",txtfiles[f])
    txtfile = txtfiles[f]
    for i in range(3,len(begs)):
        name = filename[begs[i]:fins[i]]
        OFFJets, HLTJets, MuonCollections, TrigObjs = vbf.MakeObjects(name,path)
        print("Loading objects done.")
        #ak.to_parquet(OFFJets, "./run3parquets/{0}_OFFJets{1}.parquet".format(filenames[:9], nums[i]))
        #ak.to_parquet(HLTJets, "./run3parquets/{0}_HLTJets{1}.parquet".format(filenames[:9], nums[i]))
        #ak.to_parquet(MuonCollections, "./run3parquets/{0}_MuonCollections{1}.parquet".format(filenames[:9], nums[i]))
        ak.to_parquet(TrigObjs, "./run3parquets/{0}_TrigObjs{1}.parquet".format(txtfile[:9], nums[i]))
        print("Making objects done! filename: ", "{0}_OFFJets{1}.parquet".format(txtfile[:9], nums[i]))
        print("\n")
