"""
    Light-weight efficiency analyzer for VBF SUEP MC samples in 2023.
    Raymond Kil, 2024
"""

import os, json
import uproot, vector
import numpy as np
import awkward as ak
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")

parser.add_option('--triggerpath', dest='triggerpath', default='pt105', type=str           , help='options: pt105, pt125.')
parser.add_option('--analysis'   , dest='analysis'   , default='mjj'  , type=str           , help='variable to analyze. Options: leadpt, subleadpt, mjj, deta.')
parser.add_option('--tightcuts'  , dest='tightcuts'  , default=False  , action='store_true', help='tight cuts.')
parser.add_option('--nanodir'    , dest='nanodir'    , default='.'    , type=str           , help='directory where nanoaod files are. End with /.')
parser.add_option('--outputdir'  , dest='outputdir'  , default='.'    , type=str           , help='path to directory of output json. End with /.')
(options, args) = parser.parse_args()

triggerpath = options.triggerpath
analysis    = options.analysis
tightcuts   = options.tightcuts
nanodir     = options.nanodir
outputdir   = options.outputdir

if triggerpath=='pt105':
    triggerdict = {
        "leadjetpt": 105,
        "subleadjetpt": 40,
        "mjj": 1000,
        "deta": 3.5,
        "chEmEF": 0.99,
        "chHEF": 0.2,
        "neEmEF": 0.99,
        "neHEF": 0.9,
    }
    if tightcuts:
        if analysis!="leadpt"   : triggerdict.update({"leadjetpt": 130})
        if analysis!="subleadpt": triggerdict.update({"subleadjetpt": 60})
        if analysis!="mjj"      : triggerdict.update({"mjj": 1300})
        if analysis!="deta"     : triggerdict.update({"deta": 3.7})
elif triggerpath=='pt125':
    triggerdict = {
        "leadjetpt": 125,
        "subleadjetpt": 45,
        "mjj": 720,
        "deta": 3.0,
        "chEmEF": 0.99,
        "chHEF": 0.2,
        "neEmEF": 0.99,
        "neHEF": 0.9,
    }
    if tightcuts:
        if analysis!="leadpt"   : triggerdict.update({"leadjetpt": 130})
        if analysis!="subleadpt": triggerdict.update({"subleadjetpt": 60})
        if analysis!="mjj"      : triggerdict.update({"mjj": 1000})
        if analysis!="deta"     : triggerdict.update({"deta": 3.5})

numerator, denominator = [],[]

for idx, nanoaod in enumerate([n for n in os.listdir(nanodir) if 'nanoaod' in n]):
    print(f'working on file {nanoaod}...')
    with uproot.open(f"{nanodir}{nanoaod}") as nano:
        events = vector.zip({
            "pt"    : nano["Events"]["Jet_pt"].array(),
            "eta"   : nano["Events"]["Jet_eta"].array(),
            "phi"   : nano["Events"]["Jet_phi"].array(),
            "mass"  : nano["Events"]["Jet_mass"].array(),

            "jetId" : nano["Events"]["Jet_jetId"].array(),
            "chEmEF": nano["Events"]["Jet_chEmEF"].array(),
            "chHEF" : nano["Events"]["Jet_chHEF"].array(),
            "neEmEF": nano["Events"]["Jet_neEmEF"].array(),
            "neHEF" : nano["Events"]["Jet_neHEF"].array(),

            "HLT_pt105": nano["Events"]["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5"].array(),
            "HLT_pt105triple": nano["Events"]["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5_TriplePFJet"].array(),
            "HLT_pt125": nano["Events"]["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0"].array(),
            "HLT_pt125triple": nano["Events"]["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0_TriplePFJet"].array(),
        })

    if idx%100==0: print(f'number of events before jetId cut: {len(events)}')
    events = events[events.jetId >= 2]
    if idx%100==0: print(f'number of events after  jetId cut: {len(events)}')
    de, ef = (abs(events.eta) < 2.4), (triggerdict["chEmEF"] > events.chEmEF)
    events = events[(de & ef) | (~de & ef) | (~de & ~ef)]
    de, ef = (abs(events.eta) < 2.4), (triggerdict["chHEF"] > events.chHEF)
    events = events[(de & ef) | (~de & ef) | (~de & ~ef)]
    de, ef = (abs(events.eta) < 2.4), (triggerdict["neEmEF"] > events.neEmEF)
    events = events[(de & ef) | (~de & ef) | (~de & ~ef)]
    de, ef = (abs(events.eta) < 2.4), (triggerdict["neHEF"] > events.neHEF)
    events = events[(de & ef) | (~de & ef) | (~de & ~ef)]
    events = events[ak.num(events.jetId)>=2]
    if idx%100==0: print(f'number of events after  EF cuts: {len(events)}')

    jetcombo = ak.combinations(events,2, fields=["jet1","jet2"])
    if analysis != 'leadpt'   : 
        jetcombo = jetcombo[jetcombo.jet1.pt >= triggerdict["leadjetpt"]]
        if idx%100==0: print(f'number of nonzero events after leadpt cut: {ak.count_nonzero(ak.num(jetcombo.jet1.pt))}')
    if analysis != 'subleadpt': 
        jetcombo = jetcombo[jetcombo.jet2.pt >= triggerdict["subleadjetpt"]]
        if idx%100==0: print(f'number of nonzero events after subleadpt cut: {ak.count_nonzero(ak.num(jetcombo.jet1.pt))}')
    if analysis != 'mjj'      : 
        jetcombo = jetcombo[(jetcombo.jet1+jetcombo.jet2).mass >= triggerdict["mjj"]]
        if idx%100==0: print(f'number of nonzero events after mjj cut: {ak.count_nonzero(ak.num(jetcombo.jet1.pt))}')
    if analysis != 'deta'     : 
        jetcombo = jetcombo[abs(vector.Spatial.deltaeta(jetcombo.jet1, jetcombo.jet2)) >= triggerdict["deta"]]
        if idx%100==0: print(f'number of nonzero events after deta cut: {ak.count_nonzero(ak.num(jetcombo.jet1.pt))}')

    survived = ak.where(ak.num(jetcombo.jet1.pt)>0,True,False)
    events, jetcombo = events[survived], jetcombo[survived]
    if idx%100==0: print(f'number of events after survival cuts: {len(events)}')

    maxmjjarg = ak.argmax((jetcombo.jet1+jetcombo.jet2).mass, axis=1)
    if len(maxmjjarg)>1: denom_jetcombo = jetcombo[ak.unflatten(maxmjjarg,1)]
    else: denom_jetcombo = jetcombo[maxmjjarg]

    if triggerpath=='pt105': numer_jetcombo = denom_jetcombo[((denom_jetcombo.jet1.HLT_pt105)&(denom_jetcombo.jet2.HLT_pt105))|((denom_jetcombo.jet1.HLT_pt105triple)&(denom_jetcombo.jet2.HLT_pt105triple))]
    if triggerpath=='pt125': numer_jetcombo = denom_jetcombo[(denom_jetcombo.jet1.HLT_pt125)&(denom_jetcombo.jet2.HLT_pt125)|((denom_jetcombo.jet1.HLT_pt125triple)&(denom_jetcombo.jet2.HLT_pt125triple))]

    if   analysis=='leadpt'   : denom, numer = ak.flatten(denom_jetcombo.jet1.pt), ak.flatten(numer_jetcombo.jet1.pt)
    elif analysis=='subleadpt': denom, numer = ak.flatten(denom_jetcombo.jet2.pt), ak.flatten(numer_jetcombo.jet2.pt)
    elif analysis=='mjj'      : denom, numer = ak.flatten((denom_jetcombo.jet1 + denom_jetcombo.jet2).mass), ak.flatten((numer_jetcombo.jet1 + numer_jetcombo.jet2).mass)
    elif analysis=='deta'     : denom, numer = ak.flatten(abs(vector.Spatial.deltaeta(denom_jetcombo.jet1, denom_jetcombo.jet2))), ak.flatten(abs(vector.Spatial.deltaeta(numer_jetcombo.jet1, numer_jetcombo.jet2)))
    numerator.extend(list(numer))
    denominator.extend(list(denom))
    print('\n')

quantity_dict = {
    "numerator"  : numerator,
    "denominator": denominator
}

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer) : return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray) : return obj.tolist()
        return super(NpEncoder, self).default(obj)

if not os.path.exists(outputdir): os.mkdir(outputdir)
cuts = 'tight' if tightcuts else 'loose'
with open(f'{outputdir}M125genericT2_{analysis}_{triggerpath}_{cuts}.json', 'w') as j: json.dump(quantity_dict, j,cls=NpEncoder, indent=2)
print(f'JSON made! Location: {outputdir}M125genericT2_{analysis}_{triggerpath}_{cuts}.json')