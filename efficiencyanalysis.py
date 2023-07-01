import numpy as np
import awkward as ak
import uproot
import vector
import mplhep as hep
import matplotlib.pyplot as plt
import os
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
from scipy.stats import beta

### FUNCTION DEFINITION ###
def GetMaxMjj(Jets):
    jetcombo = ak.combinations(Jets,2, fields=["jet1","jet2"])
    jjsum  = jetcombo.jet1 + jetcombo.jet2
    maxmjj   = ak.max(jjsum.mass,axis=1)
    maxmjjindex = ak.Array(ak.to_list(np.expand_dims(ak.argmax(jjsum.mass,axis=1),axis=1)))
    maxmjjpair = jetcombo[maxmjjindex]
    return maxmjj, maxmjjpair # Retriving jets: maxmjjpair.jet1 ...

def GetMaxEta(Jets):
    JetCombo = ak.combinations(Jets,2, fields=["jet1","jet2"])
    etacombo = vector.Spatial.deltaeta(JetCombo.jet1, JetCombo.jet2)
    maxeta   = ak.max(abs(etacombo), axis=1)
    return maxeta

def clopper_pearson_interval(hltPassed, total, alpha):
    min, max = beta.ppf(alpha, hltPassed, total - hltPassed + 1), beta.ppf(1 - alpha, hltPassed + 1, total - hltPassed)
    center = 0
    if total !=0: center = hltPassed/total
    min, max = center-min , max-center
    return min, max

def DoCuts(OFFJets, HLTJets, MuonCollections, cut):
    OFFJets = OFFJets[cut]
    HLTJets = HLTJets[cut]
    MuonCollections = MuonCollections[cut]
    return OFFJets, HLTJets, MuonCollections

def ApplyBasicCuts(OFFJets, HLTJets, MuonCollections):
    print("number of events before BasicCuts: {}".format(len(OFFJets)))
    
    nJetCut = (ak.num(OFFJets)>=2)
    OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, nJetCut)
    print("number of events after nJetCut: {}".format(len(OFFJets)))

    MuonPtCut = (ak.any(MuonCollections.Muon_pt>=27 & MuonCollections.muRelIso<0.2, axis=1))
    OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, MuonPtCut)
    print("number of events after MuonPtCut: {}".format(len(OFFJets)))

    IsoMu24Cut = HLTJets.IsoMu24
    OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, IsoMu24Cut)
    print("number of events after IsoMu24Cut: {}".format(len(OFFJets)))

    # This cut is now passing an event if it has at least one (reasonably, i.e., muRelIso<0.2) isolated muon 
    """
    RelIso04Cut = (ak.any(MuonCollections.muRelIso<0.2, axis=1))
    OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, RelIso04Cut)
    print("number of events after RelIso04Cut: {}".format(len(OFFJets)))
    """
    return OFFJets, HLTJets, MuonCollections

def ApplyTriggerCuts(OFFJets, HLTJets, MuonCollections, analysis, triggerdict):
    print("number of events before TriggerCuts: {}".format(len(OFFJets)))

    # single jet criteria
    if analysis!="LeadJetPtAnalysis":
        leadptCut = (OFFJets.pt[:,0]>=triggerdict["leadjetpt"])
        OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, leadptCut)
        print("number of events after leadptCut: {}".format(len(OFFJets)))

    if analysis!="SubleadJetPtAnalysis":
        subleadptCut = (OFFJets.pt[:,1]>triggerdict["subleadjetpt"])
        OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, subleadptCut)
        print("number of events after subleadptCut: {}".format(len(OFFJets)))

# the jets that produces the maxmjj should pass the leadptCut and subleadptCut


    # dijet criteria
    OFFmjj, maxmjjpair = GetMaxMjj(OFFJets)
    OFFdEta = ak.flatten(vector.Spatial.deltaeta(maxmjjpair.jet1, maxmjjpair.jet2))

    if analysis!="MjjAnalysis":
        OFFmjjCut = (OFFmjj >= triggerdict["mjj"])
        OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, OFFmjjCut)
        maxmjjpair = maxmjjpair[OFFmjjCut]
        OFFdEta = OFFdEta[OFFmjjCut]
        print("number of events after OFFmjjCut: {}".format(len(OFFJets)))

    if analysis!="DetaAnalysis":
        OFFdEtaCut = (OFFdEta >= triggerdict["deta"])
        OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, OFFdEtaCut)
        print("number of events after OFFdetaCut: {}".format(len(OFFJets)))

    return OFFJets, HLTJets, MuonCollections

def GetEfficiency(binsize, maxbin, HLTPassedQuantity, OFFJetQuantity):
    bincenters = np.arange(binsize,maxbin,2*binsize)
    effs = np.zeros(len(bincenters))
    errmin,errmax = np.zeros(len(bincenters)), np.zeros(len(bincenters))

    for i in range(len(bincenters)):
        minlim = round(bincenters[i] - binsize,5)
        maxlim = round(bincenters[i] + binsize,5)

        nHLT = ak.count_nonzero(ak.where((HLTPassedQuantity>minlim) & (HLTPassedQuantity<=maxlim), 1, 0))
        nOFF = ak.count_nonzero(ak.where((OFFJetQuantity   >minlim) & (OFFJetQuantity   <=maxlim), 1, 0))
        print(minlim, maxlim, nHLT, nOFF)
        errmin[i],errmax[i] = clopper_pearson_interval(nHLT,nOFF,0.05)
        if nOFF!=0: effs[i] = nHLT/nOFF
    yerrmin, yerrmax = np.nan_to_num(errmin), np.nan_to_num(errmax)

    return effs, yerrmin, yerrmax, bincenters

### PREPROCESSING ###
parser.add_option("--whichfiles" , dest="whichfiles" , default="singlemuon"       , help="options: singlemuon, zerobias")
parser.add_option("--triggerpath", dest="triggerpath", default="pt105Analysis"    , help="options: pt105Analysis, pt125Analysis")
parser.add_option("--analysis"   , dest="analysis"   , default="LeadJetPtAnalysis", help="options: LeadJetPtAnalysis, SubleadJetPtAnalysis, MjjAnalysis, DetaAnalysis")
parser.add_option("--tightcuts"  , dest="tightcuts"  , default=False              , help="options: True, False")
(options, args) = parser.parse_args()

whichfiles  = options.whichfiles
triggerpath = options.triggerpath
analysis    = options.analysis
TightCuts   = options.tightcuts

if whichfiles=="singlemuon":
    path = "/eos/user/j/jkil/SUEP/suep-production/summer23data/singlemuon/"
    #path = "/Users/raymondkil/Desktop/vbftrigger/effrootfiles/singlemuon/"
    datasetname = "SingleMuon"
if whichfiles=="zerobias":
    path = "/eos/user/j/jkil/SUEP/suep-production/summer23data/zerobias/"
    datasetname = "ZeroBias"
names = os.listdir(path)[:10]
#names = [x for x in os.listdir(path) if x != '.DS_Store']

if triggerpath=="pt105Analysis":
    triggerdict = {
        "leadjetpt": 105,
        "subleadjetpt": 40,
        "mjj": 1000,
        "deta": 3.5,
    }

if triggerpath=="pt125Analysis":
    triggerdict = {
        "leadjetpt": 125,
        "subleadjetpt": 45,
        "mjj": 720,
        "deta": 3.0,
    }

if TightCuts:  # This is where I update the cuts!
    if triggerpath=="pt105Analysis":
        if analysis!="LeadJetPtAnalysis"   : triggerdict.update({"leadjetpt": 130})
        if analysis!="SubleadJetPtAnalysis": triggerdict.update({"subleadjetpt": 60})
        if analysis!="MjjAnalysis"         : triggerdict.update({"mjj": 1300})
        if analysis!="DetaAnalysis"        : triggerdict.update({"deta": 3.8})
    if triggerpath=="pt125Analysis":
        if analysis!="LeadJetPtAnalysis"   : triggerdict.update({"leadjetpt": 130})
        if analysis!="SubleadJetPtAnalysis": triggerdict.update({"subleadjetpt": 60})
        if analysis!="MjjAnalysis"         : triggerdict.update({"mjj": 1300})
        if analysis!="DetaAnalysis"        : triggerdict.update({"deta": 3.8})


### PROCESSING ###
OFFJets, HLTJets, MuonCollections = [],ak.Array([]), []
for filename in names:
    print("Processing file {0}".format(filename))
    f = uproot.open(path + filename)
    events = f["Events"]

    HLTJet = ak.zip({ # Regular array corresponding to events...... Maybe change the name to HLTPath(s) for more intuition
        "pt105":       events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5"].array(),
        "pt105triple": events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5_TriplePFJet"].array(),
        "pt125":       events["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0"].array(),
        "pt125triple": events["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0_TriplePFJet"].array(),

        "IsoMu24": events["HLT_IsoMu24"].array(), #[True, True, True, True, True, False, ... False, False, False, True, True, False]]
    })

    OFFJet = vector.zip({ # Jagged array with subarrays corresponding to jets
        "pt": events["Jet_pt"].array(),
        "eta": events["Jet_eta"].array(),
        "phi": events["Jet_phi"].array(),
        "mass": events["Jet_mass"].array(),

        "chEmEF": events["Jet_chEmEF"].array(),
        "chHEF": events["Jet_chHEF"].array(),
        "neEmEF": events["Jet_neEmEF"].array(),
        "neHEF": events["Jet_neHEF"].array(),
        "muEF": events["Jet_muEF"].array(),
    })

    MuonCollection = ak.zip({ # Jagged array with subarrays corresponding to muons
        "nMuon": events["nMuon"].array(),
        "Muon_pt": events["Muon_pt"].array(),
        "muRelIso": events["Muon_pfRelIso04_all"].array() # relative isolation of muons [[0.0981], [0.0469, 0.362], [0.0085, ... 0.0036], [0.251, 0, 0.254, 0.412, 0.87]]
    })

    OFFJets = ak.concatenate((OFFJets, OFFJet))
    HLTJets = ak.concatenate((HLTJets, HLTJet))
    MuonCollections = ak.concatenate((MuonCollections, MuonCollection))

# cuts
OFFJets, HLTJets, MuonCollections = ApplyBasicCuts(OFFJets, HLTJets, MuonCollections)
OFFJets, HLTJets, MuonCollections = ApplyTriggerCuts(OFFJets, HLTJets, MuonCollections, analysis, triggerdict)
if   triggerpath=="pt105Analysis": HLTpassedJets = OFFJets[HLTJets.pt105|HLTJets.pt105triple]
elif triggerpath=="pt125Analysis": HLTpassedJets = OFFJets[HLTJets.pt125|HLTJets.pt125triple]

print("Number of events that passed HLT: {}".format(len(HLTpassedJets)))
print("Number of offline events: {}".format(len(OFFJets)))

### POSTPROCESSING ###
if analysis=="LeadJetPtAnalysis":
    vardict = {
        "plotname": "leadpt",
        "binsize"  : 5,
        "HLTPassedQuantity": HLTpassedJets.pt[:,0],
        "OFFJetQuantity": OFFJets.pt[:,0],
        "maxbin": 210,
        "xlabel": r"Offline $p_T^{leadjet}$ (GeV)",
        "threshold": triggerdict["leadjetpt"],
    }

if analysis=="SubleadJetPtAnalysis":
    vardict = {
        "plotname": "subleadpt",
        "binsize"  : 2,
        "HLTPassedQuantity": HLTpassedJets.pt[:,1],
        "OFFJetQuantity": OFFJets.pt[:,1],
        "maxbin": 100,
        "xlabel": r"Offline $p_T^{subleadjet}$ (GeV)",
        "threshold": triggerdict["subleadjetpt"],
    }

if analysis=="MjjAnalysis":
    vardict = {
        "plotname": "mjj",
        "binsize"  : 50,
        "HLTPassedQuantity": GetMaxMjj(HLTpassedJets),
        "OFFJetQuantity": GetMaxMjj(OFFJets),
        "maxbin": 2000,
        "xlabel": r"Offline $M_{jj}$ (GeV)",
        "threshold": triggerdict["mjj"],
    }

if analysis=="DetaAnalysis":
    vardict = {
        "plotname": "deta",
        #"binsize"  : 0.1,
        "binsize"  : 10.0,
        "HLTPassedQuantity": GetMaxEta(HLTpassedJets),
        "OFFJetQuantity": GetMaxEta(OFFJets),
        "maxbin": 12.0,
        "xlabel": r"Offline $\Delta\eta$",
        "threshold": triggerdict["deta"],
    }

### EFFICIENCY ###
effs, yerrmin, yerrmax, bincenters = GetEfficiency(vardict["binsize"], vardict["maxbin"], vardict["HLTPassedQuantity"], vardict["OFFJetQuantity"])


### PLOTTING ###
# if triggerpath=="pt105Analysis": pltPath = "/eos/user/j/jkil/www/VBFSUEP/efficiency/pt105/"
# if triggerpath=="pt125Analysis": pltPath = "/eos/user/j/jkil/www/VBFSUEP/efficiency/pt125/"
# if triggerpath=="pt105Analysis": pltPath = "/eos/user/j/jkil/www/VBFSUEP/efficiency/dijet/"
#pltPath = "/Users/raymondkil/Desktop/vbftrigger/plots/"
pltPath = "/eos/user/j/jkil/www/VBFSUEP/efficiency/withBasicCuts/"
plt.style.use(hep.style.CMS)
plt.figure()

plt.errorbar(bincenters,effs, yerr=[yerrmin,yerrmax], xerr=vardict["binsize"], marker='o', color="black", label="Efficiency", linestyle='')
plt.xlabel(vardict["xlabel"])
plt.ylabel("Efficiency")
plt.ylim(-0.06,1.2)
hep.cms.text("Preliminary")
hep.cms.lumitext(r"Summer23 (L=1.01 fb$^{-1}$)")
plt.axvline(x=vardict["threshold"], color='tab:red', label="Threshold", linestyle="--")

plt.text(0,1.0,"dataset: {}".format(datasetname), size='x-small', color='steelblue')
if analysis!="LeadJetPtAnalysis":    plt.text(0,0.95,"leadptcut: {}".format(triggerdict["leadjetpt"]), size='x-small', color='steelblue')
if analysis!="SubleadJetPtAnalysis": plt.text(0,0.9,"subleadptcut: {}".format(triggerdict["subleadjetpt"]), size='x-small', color='steelblue')
if analysis!="MjjAnalysis":          plt.text(0,0.85,"mjjcut: {}".format(triggerdict["mjj"]), size='x-small', color='steelblue')
if analysis!="DetaAnalysis":         plt.text(0,0.8,"detacut: {}".format(triggerdict["deta"]), size='x-small', color='steelblue')

plt.legend(loc=2)
plt.grid()
if TightCuts:
    plt.savefig("{0}{1}{2}TightEff.png".format(pltPath,datasetname,vardict["plotname"]))
    print("Plots made! Name: {0}{1}{2}TightEff.png".format(pltPath,datasetname,vardict["plotname"]))
else:
    plt.savefig("{0}{1}{2}Eff.png".format(pltPath,datasetname,vardict["plotname"]))
    print("Plots made! Name: {0}{1}{2}Eff.png".format(pltPath,datasetname,vardict["plotname"]))
