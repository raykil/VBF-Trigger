import os
import definitions as vbf
import awkward as ak
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")

parser.add_option("--begin", dest="begin" , default=0  , help="options: singlemuon, zerobias")
parser.add_option("--end"  , dest="end" , default=30 , help="options: singlemuon, zerobias")
(options, args) = parser.parse_args()
i = options.begin
f = options.end

path = "/eos/user/j/jkil/SUEP/suep-production/summer23data/singlemuon/"
names = os.listdir(path)[int(i):int(f)]
# [:30], [30:60], [60:90], [90:120], [120:]

OFFJets, HLTJets, MuonCollections = vbf.MakeObjects(names, path)
print("Loading objects done.")

ak.to_parquet(OFFJets, "/eos/user/j/jkil/SUEP/suep-production/run3parquets/run3singlemuon_OFFJets" + i + f + ".parquet")
ak.to_parquet(HLTJets, "/eos/user/j/jkil/SUEP/suep-production/run3parquets/run3singlemuon_HLTJets" + i + f + ".parquet")
ak.to_parquet(MuonCollections, "/eos/user/j/jkil/SUEP/suep-production/run3parquets/run3singlemuon_MuonCollections" + i + f + ".parquet")
print("Making objects done!")