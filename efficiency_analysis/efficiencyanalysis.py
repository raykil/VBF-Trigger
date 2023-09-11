"""
    This program calculates and plots the efficiency for VBF trigger path.
    Raymond Kil, 2023
"""

import awkward as ak
import vector
import mplhep as hep
import matplotlib.pyplot as plt
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
from scipy.stats import beta
import definitions as vbf
import numpy as np

### PREPROCESSING ###
parser.add_option("--whichfiles" , dest="whichfiles" , default="singlemuon"                           , help="options: singlemuon, zerobias")
parser.add_option("--triggerpath", dest="triggerpath", default="pt105Analysis"                        , help="options: pt105Analysis, pt125Analysis")
parser.add_option("--analysis"   , dest="analysis"   , default="LeadJetPtAnalysis"                    , help="options: LeadJetPtAnalysis, SubleadJetPtAnalysis, MjjAnalysis, DetaAnalysis")
parser.add_option("--tightcuts"  , dest="tightcuts"  , default=False                                  , help="options: True, False")
parser.add_option("--outputdir"  , dest="outputdir"  , default="/Users/raymondkil/Desktop/vbftrigger/" , help="output directory")
parser.add_option("--shape"      , dest="shape"      , default=False , help="produce histograms of property distribution")
parser.add_option("--datapath"   , dest="datapath"   , default="./" , help="directory where the parquet files are in")
(options, args) = parser.parse_args()

whichfiles  = options.whichfiles
triggerpath = options.triggerpath
analysis    = options.analysis
TightCuts   = options.tightcuts
outputdir   = options.outputdir
shapeAnalysis = options.shape
datapath = options.datapath

if whichfiles=="singlemuon":
    path = datapath
    datasetname = "SingleMuon"
    OFFJets = ak.from_parquet(path + "*OFFJets*.parquet")
    HLTJets = ak.from_parquet(path + "*HLTJets*.parquet")
    MuonCollections = ak.from_parquet(path + "*MuonCollections*.parquet")
    TrigObjs = ak.from_parquet(path + "*TrigObjs*.parquet")
    OFFJets = vector.zip({
            "pt": OFFJets.rho,
            "eta": OFFJets.eta,
            "phi": OFFJets.phi,
            "mass": OFFJets.tau,
            "nTracks": OFFJets.nTracks,

            "chEmEF": OFFJets.chEmEF,
            "chHEF": OFFJets.chHEF,
            "neEmEF": OFFJets.neEmEF,
            "neHEF": OFFJets.neHEF,
            "muEF": OFFJets.muEF,
        })
    print(f"Successfully loaded objects using parquet! Number of events: {len(OFFJets)}")
if whichfiles=="zerobias":
    path = "/eos/user/j/jkil/SUEP/suep-production/summer23data/zerobias/"
    datasetname = "ZeroBias"

if triggerpath=="pt105Analysis":
    triggerdict = {
        "leadjetpt": 105,
        "subleadjetpt": 40,
        "mjj": 1000,
        "deta": 3.5,
        "chEmEF": 0.99,
        "chHEF": 0.2,
        "neEmEF": 0.99,
        "neHEF": 0.9
    }

if triggerpath=="pt125Analysis":
    triggerdict = {
        "leadjetpt": 125,
        "subleadjetpt": 45,
        "mjj": 720,
        "deta": 3.0,
        "chEmEF": 0.99,
        "chHEF": 0.2,
        "neEmEF": 0.99,
        "neHEF": 0.9
    }

if TightCuts:  # This is where I update the cuts!
    if triggerpath=="pt105Analysis":
        if analysis!="LeadJetPtAnalysis"   : triggerdict.update({"leadjetpt": 130})
        if analysis!="SubleadJetPtAnalysis": triggerdict.update({"subleadjetpt": 60})
        if analysis!="MjjAnalysis"         : triggerdict.update({"mjj": 1300})
        if analysis!="DetaAnalysis"        : triggerdict.update({"deta": 3.7})
    if triggerpath=="pt125Analysis":
        if analysis!="LeadJetPtAnalysis"   : triggerdict.update({"leadjetpt": 130})
        if analysis!="SubleadJetPtAnalysis": triggerdict.update({"subleadjetpt": 60})
        if analysis!="MjjAnalysis"         : triggerdict.update({"mjj": 1300})
        if analysis!="DetaAnalysis"        : triggerdict.update({"deta": 3.7})


### PROCESSING ###

basicOFFJets, basicHLTJets, basicMuonCollections, basicTrigObjs = vbf.ApplyBasicCuts(OFFJets, HLTJets, MuonCollections, TrigObjs, analysis, triggerdict)
cleanOFFJets, cleanHLTJets, cleanMuonCollections, cleanTrigObjs, cleanOFFcombo = vbf.ApplyTriggerCuts(basicOFFJets, basicHLTJets, basicMuonCollections, basicTrigObjs, analysis, triggerdict)
HLTCandJets, HLTCandMaxMjjCombo, shouldPassHLT_mjjs, shouldPassHLT_detas = vbf.SelectHLTJetsCand(cleanOFFJets, cleanOFFcombo)
assigned_TrigObjs, assigned_OFFJets, HLTPassed_OFFJets = vbf.AssignFilterBitsToOFFJets(cleanTrigObjs, HLTCandJets, cleanHLTJets, triggerpath)

print("\n")
print(f"Number of events that passed HLT: {len(HLTPassed_OFFJets)}")
print(f"Number of offline events: {len(HLTCandJets)}")

### POSTPROCESSING ###
vardict = vbf.GetVardict(HLTPassed_OFFJets, HLTCandJets, analysis, triggerdict, shouldPassHLT_mjjs, shouldPassHLT_detas)

### EFFICIENCY ###
effs, yerrmin, yerrmax, bincenters = vbf.GetEfficiency(vardict["binsize"], vardict["maxbin"], vardict["HLTPassedQuantity"], vardict["HLTCandQuantity"])

### PLOTTING ###
pltPath = outputdir
plt.style.use(hep.style.CMS)
fig = plt.figure()

plt.errorbar(bincenters,effs, yerr=[yerrmin,yerrmax], xerr=vardict["binsize"], marker='o', color="black", label="Efficiency", linestyle='')
plt.xlabel(vardict["xlabel"])
plt.ylabel("Efficiency")
plt.ylim(-0.06,1.2)
hep.cms.text("Preliminary")
hep.cms.lumitext(r"Summer23 (L=12.98 fb$^{-1}$)")
if analysis in ["LeadJetPtAnalysis", "SubleadJetPtAnalysis", "MjjAnalysis", "DetaAnalysis"]:
    plt.axvline(x=vardict["threshold"], color='tab:red', label="Threshold", linestyle="--")

#plt.text(0,1.0,"dataset: {}".format(datasetname), size='x-small', color='steelblue')
plt.text(0.2, 0.7,r"$\geq 1$ tight $\mu$ ($p_T\geq 27$ GeV), pass HLT_IsoMu24", ha='left', va='top', size='x-small', color='red', transform=fig.transFigure)
txtcount = 0
cutyloc = [0.65,0.6,0.55,0.5]
if analysis!="LeadJetPtAnalysis":    
    plt.text(0.2, cutyloc[txtcount], f"leadptcut: {triggerdict['leadjetpt']}"      , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
    txtcount += 1
if analysis!="SubleadJetPtAnalysis": 
    plt.text(0.2, cutyloc[txtcount], f"subleadptcut: {triggerdict['subleadjetpt']}", ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
    txtcount += 1
if analysis!="MjjAnalysis":          
    plt.text(0.2, cutyloc[txtcount], f"mjjcut: {triggerdict['mjj']}"               , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
    txtcount += 1
if analysis!="DetaAnalysis":         
    plt.text(0.2, cutyloc[txtcount], f"detacut: {triggerdict['deta']}"             , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
    txtcount += 1

plt.text(0.85,0.84, r"$N_{off/HLT} = $"+str(len(HLTPassed_OFFJets)), ha='right', size='x-small', color='cadetblue', transform=fig.transFigure)
plt.text(0.85,0.8, r"$N_{off} = $"+str(len(HLTCandJets)), ha='right', size='x-small', color='cadetblue', transform=fig.transFigure)

plt.legend(loc=2)
plt.grid()
if TightCuts:
    plt.savefig(f"{pltPath}{vardict['plotname']}_Tight.png")
    print(f"Efficiency plots made! Name: {pltPath}{vardict['plotname']}_TightEff.png")
else:
    plt.savefig(f"{pltPath}{vardict['plotname']}.png")
    print(f"Efficiency plots made! Name: {pltPath}{vardict['plotname']}_Eff.png")


### SHAPES ###
if shapeAnalysis:
    xlim = vardict["maxbin"]
    binsize = vardict["binsize"]
    cands = vardict["HLTCandQuantity"]
    passd = vardict["HLTPassedQuantity"]
    plt.style.use(hep.style.CMS)
    fig = plt.figure()
    candsHist, candsBins = np.histogram(cands, bins=np.arange(0,xlim+binsize,binsize))
    passdHist, passdBins = np.histogram(passd, bins=np.arange(0,xlim+binsize,binsize))
    hep.histplot(candsHist, candsBins, histtype='step', label=f"cands {analysis[:-8]}", color="tab:blue", density=False, stack=True)
    hep.histplot(passdHist, passdBins, histtype='step', label=f"passed {analysis[:-8]}", color="tab:orange", density=False, stack=True, linestyle='--')
    hep.cms.text("Preliminary")
    hep.cms.lumitext(r"Summer23 (L=12.98 fb$^{-1}$)")
    plt.xlabel(vardict["xlabel"])
    plt.ylabel(r"Counts")
    if analysis!="LeadJetPtAnalysis":    plt.text(0.2, 0.65, f"leadptcut: {triggerdict['leadjetpt']}"      , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
    if analysis!="SubleadJetPtAnalysis": plt.text(0.2, 0.6 , f"subleadptcut: {triggerdict['subleadjetpt']}", ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
    if analysis!="MjjAnalysis":          plt.text(0.2, 0.55, f"mjjcut: {triggerdict['mjj']}"               , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
    if analysis!="DetaAnalysis":         plt.text(0.2, 0.5 , f"detacut: {triggerdict['deta']}"             , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
    if analysis in ["LeadJetPtAnalysis", "SubleadJetPtAnalysis", "MjjAnalysis", "DetaAnalysis"]:
        plt.axvline(x=vardict["threshold"], color='tab:red', label="Threshold", linestyle="--")
    plt.text(0.85,0.84, r"$N_{off/HLT} = $"+str(len(passd)), ha='right', size='x-small', color='cadetblue', transform=fig.transFigure)
    plt.text(0.85,0.8, r"$N_{off} = $"+str(len(cands)), ha='right', size='x-small', color='cadetblue', transform=fig.transFigure)
    plt.legend()
    plt.grid()
    if TightCuts:
        plt.savefig(f"{pltPath}{analysis[:-8]}_TightShape.png")
        print(f"Shape plots made! Name: {pltPath}{analysis[:-8]}_TightShape.png")
    else:
        plt.savefig(f"{pltPath}{analysis[:-8]}_Shape.png")
        print(f"Shape plots made! Name: {pltPath}{analysis[:-8]}_Shape.png")