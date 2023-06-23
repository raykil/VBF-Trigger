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
    JetCombo = ak.combinations(Jets,2, fields=["jet1","jet2"])
    jjCombo  = JetCombo.jet1 + JetCombo.jet2
    mjjCombo = np.sqrt(np.abs((jjCombo.E)**2 - (jjCombo.px**2 + jjCombo.py**2 + jjCombo.pz**2)))
    maxmjj   = ak.max(mjjCombo,axis=1)
    return maxmjj

def GetMaxEta(Jets):
    JetCombo = ak.combinations(Jets,2, fields=["jet1","jet2"])
    etacombo = vector.Spatial.deltaeta(JetCombo.jet1, JetCombo.jet2)
    maxeta   = ak.max(abs(etacombo), axis=1)
    return maxeta

def clopper_pearson_interval(hltPassed, total, confidence):
    alpha = (1 - confidence) / 2
    min = beta.ppf(alpha, hltPassed, total - hltPassed + 1)
    max = beta.ppf(1 - alpha, hltPassed + 1, total - hltPassed)
    center = 0
    if total !=0: center = hltPassed/total
    min = center - min
    max = max - center
    return min, max

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
    datasetname = "SingleMuon"
if whichfiles=="zerobias": 
    path = "/eos/user/j/jkil/SUEP/suep-production/summer23data/zerobias/"
    datasetname = "ZeroBias"
names = os.listdir(path)[:10]

# Trigger path dictionaries (before processing)
# Remember, I should change the values for the vars that I am NOT plotting. Double check the "Which Analysis?" part.

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

if TightCuts: # This is where I update the cuts!
    if analysis!="LeadJetPtAnalysis"   : triggerdict.update({"leadjetpt": 130})
    if analysis!="SubleadJetPtAnalysis": triggerdict.update({"subleadjetpt": 45})
    if analysis!="MjjAnalysis"         : triggerdict.update({"mjj": 1000})
    if analysis!="DetaAnalysis"        : triggerdict.update({"deta": 4.0})

### PROCESSING ###

mjjs, dEtas, HLTpassedJets, OFFJets = [],[],[],[]

for filename in names:
    print("Processing file {0}".format(filename))
    f = uproot.open(path + filename)
    events = f["Events"]
    HLTJets = ak.zip({
        "pt105":       events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5"].array(),
        "pt105triple": events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5_TriplePFJet"].array(),
        "pt125":       events["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0"].array(),
        "pt125triple": events["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0_TriplePFJet"].array()
    })

    OFFJet = vector.zip({
        "pt": events["Jet_pt"].array(),
        "eta": events["Jet_eta"].array(),
        "phi": events["Jet_phi"].array(),
        "mass": events["Jet_mass"].array()
    })
    if triggerpath=="pt105Analysis": HLTpassedJet = OFFJet[HLTJets.pt105|HLTJets.pt105triple]
    if triggerpath=="pt125Analysis": HLTpassedJet = OFFJet[HLTJets.pt125|HLTJets.pt125triple]
    HLTnJetCut = (ak.num(HLTpassedJet)>=2)
    HLTpassedJet = HLTpassedJet[HLTnJetCut]
    HLTpassedJets = np.concatenate((HLTpassedJets, HLTpassedJet))

    nJetCut = (ak.num(OFFJet)>=2)
    OFFJet = OFFJet[nJetCut]

    if analysis!="LeadJetPtAnalysis":
        leadPtCut = (ak.max(OFFJet.pt, axis=1)>=triggerdict["leadjetpt"])
        OFFJet = OFFJet[leadPtCut]

    if analysis!="SubleadJetPtAnalysis":
        subLeadPtCut = (OFFJet.pt[:,1]>triggerdict["subleadjetpt"])
        OFFJet = OFFJet[subLeadPtCut]

    if analysis!="MjjAnalysis":
        mjj  = GetMaxMjj(OFFJet) # This is calculating mjj without mjj cut.
        mjjCut = (mjj>triggerdict["mjj"])
        OFFJet = OFFJet[mjjCut]
        dEta = GetMaxEta(OFFJet)

    if analysis!="DetaAnalysis": 
        dEta = GetMaxEta(OFFJet)
        deltaEtaCut = (dEta > triggerdict["deta"])
        OFFJet = OFFJet[deltaEtaCut]
        mjj  = GetMaxMjj(OFFJet)

    mjjs    = np.concatenate((mjjs, mjj))
    dEtas   = np.concatenate((dEtas, dEta))
    OFFJets = np.concatenate((OFFJets, OFFJet))

print("number of HLT passed Jets: {}".format(len(HLTpassedJets)))
print("number of OFF Jets: {}".format(len(OFFJets)))

# Analysis variable dictionaries (after data processing)

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
        "binsize"  : 0.1,
        "HLTPassedQuantity": GetMaxEta(HLTpassedJets),
        "OFFJetQuantity": GetMaxEta(OFFJets),
        "maxbin": 7,
        "xlabel": r"Offline $\Delta\eta$",
        "threshold": triggerdict["deta"],
    }

### EFFICIENCY ###
binsize = vardict["binsize"] # Actually half of binsize
bincenter = np.arange(binsize,vardict["maxbin"],2*binsize)
effs = np.zeros(len(bincenter))
errmin,errmax = np.zeros(len(bincenter)), np.zeros(len(bincenter))

for i in range(len(bincenter)):
    minlim = bincenter[i] - binsize
    maxlim = bincenter[i] + binsize

    nHLT = ak.count_nonzero(ak.where((vardict["HLTPassedQuantity"]>=minlim) & (vardict["HLTPassedQuantity"]<maxlim), True, False))
    nOFF = ak.count_nonzero(ak.where((vardict["OFFJetQuantity"]   >=minlim) & (vardict["OFFJetQuantity"]   <maxlim), True, False))
    errmin[i],errmax[i] = clopper_pearson_interval(nHLT,nOFF,0.95)
    if nOFF!=0: effs[i] = nHLT/nOFF
errmin, errmax = np.nan_to_num(errmin), np.nan_to_num(errmax)

### PLOTTING ###
if triggerpath=="pt105Analysis": pltPath = "/eos/user/j/jkil/www/VBFSUEP/efficiency/pt105/"
if triggerpath=="pt125Analysis": pltPath = "/eos/user/j/jkil/www/VBFSUEP/efficiency/pt125/"
plt.style.use(hep.style.CMS)
plt.figure()

plt.errorbar(bincenter,effs, yerr=[errmin,errmax], marker='o', color="black", label="Efficiency", linestyle='')
plt.xlabel(vardict["xlabel"])
plt.ylabel("Efficiency")
plt.ylim(-0.06,1.2)
hep.cms.text("Preliminary")
hep.cms.lumitext(r"Run3 Summer23 (13 TeV)")
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