"""
    This program calculates and plots the efficiency for VBF trigger path. 
    Raymond Kil, 2023
"""

import mplhep as hep
import matplotlib.pyplot as plt
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
import definitions as vbf
import numpy as np

### PREPROCESSING ###
parser.add_option("--whichfiles" , dest="whichfiles" , default="singlemuon"                   , help="options: singlemuon, zerobias")
parser.add_option("--triggerpath", dest="triggerpath", default="pt105Analysis"                , help="options: pt105Analysis, pt125Analysis")
parser.add_option("--analysis"   , dest="analysis"   , default="LeadJetPtAnalysis"            , help="options: LeadJetPtAnalysis, SubleadJetPtAnalysis, MjjAnalysis, DetaAnalysis")
parser.add_option("--tightcuts"  , dest="tightcuts"  , default=False                          , help="options: True, False")
parser.add_option("--outputdir"  , dest="outputdir"  , default="/eos/user/j/jkil/www/"        , help="output directory")
parser.add_option("--shape"      , dest="shape"      , default=False                          , help="produce histograms of property distribution")
parser.add_option("--datapath"   , dest="datapath"   , default="./"                           , help="directory where the parquet files are in")
parser.add_option("--useC"       , dest="useC"       , default=False                          , help="If true, dataset C is used")
parser.add_option("--useD"       , dest="useD"       , default=False                          , help="If true, dataset D is used")
parser.add_option("--combined"   , dest="combined"   , default=False                          , help="If combined, single efficiency is plotted. If False, plots separately.")
parser.add_option("--filterbits" , dest="filterbits" , default=False                          , help="If true, filterbits are considered. If not, just the triggerpath")
parser.add_option("--subset"     , dest="subset"     , default=""                             , help="Only loads subset of the dataset. String that specifies which files to load. options: '0000', '3600'...")
parser.add_option("--goldenpath" , dest="goldenpath" , default="../luminosity/2023golden.json", help="path for goldenJSON file.")
(options, args) = parser.parse_args()

whichfiles    = options.whichfiles
triggerpath   = options.triggerpath
analysis      = options.analysis
TightCuts     = options.tightcuts
outputdir     = options.outputdir
shapeAnalysis = options.shape
datapath      = options.datapath
useC          = options.useC
useD          = options.useD
combined      = options.combined
filterbits    = options.filterbits
subset        = options.subset
goldenpath    = options.goldenpath

datasets    = vbf.LoadDataset(whichfiles, datapath, useC, useD, combined, subset)
triggerdict = vbf.GetTriggerDict(triggerpath, analysis, TightCuts)

### PROCESSING ###
pltPath = outputdir
plt.style.use(hep.style.CMS)
fig = plt.figure()
Nxloc = [0.7, 0.5]

for idx, dataset in enumerate(datasets):
    print(f"working on dataset {dataset['label']}...")
    goldenOFFJets, goldenHLTJets, goldenMuonCollections, goldenTrigObjs = vbf.MakeGolden(dataset["OFFJets"], dataset["HLTJets"], dataset["MuonCollections"], dataset["TrigObjs"], dataset["Luminosities"], goldenpath)
    basicOFFJets, basicHLTJets, basicMuonCollections, basicTrigObjs = vbf.ApplyBasicCuts(goldenOFFJets, goldenHLTJets, goldenMuonCollections, goldenTrigObjs, analysis, triggerdict)
    assigned_OFFJets, assigned_HLTJets, assigned_TrigObjs = vbf.AssignFilterBitsToOFFJets(basicOFFJets, basicHLTJets, basicTrigObjs)
    cleanOFFJets, cleanHLTJets, cleanTrigObjs, cleanOFFcombo = vbf.ApplyTriggerCuts(assigned_OFFJets, assigned_HLTJets, assigned_TrigObjs, analysis, triggerdict)
    shouldPassHLT_OFFjets, shouldPassHLT_combo = vbf.SelectHLTJetsCand(cleanOFFJets, cleanOFFcombo)
    shouldPassQuantity, passedQuantity = vbf.GetNumDenom(shouldPassHLT_OFFjets, cleanHLTJets, shouldPassHLT_combo, analysis, triggerpath, filterbits)

    print("\n")
    print(f"Number of events that passed HLT: {len(passedQuantity)}")
    print(f"Number of offline events: {len(shouldPassQuantity)}")

    vardict = vbf.GetVardict(passedQuantity, shouldPassQuantity, analysis, triggerdict)
    effs, yerrmin, yerrmax, bincenters = vbf.GetEfficiency(vardict["binsize"], vardict["maxbin"], vardict["HLTPassedQuantity"], vardict["HLTCandQuantity"])

    # plotting
    plt.errorbar(bincenters,effs, yerr=[yerrmin,yerrmax], xerr=vardict["binsize"], marker='o', color=dataset["color"], label=f"{dataset['label']} Efficiency", linestyle='')
    plt.text(Nxloc[idx],0.84, dataset['label'] + r" $N_{off/HLT} = $"+str(len(passedQuantity)), ha='left', size='x-small', color='cadetblue', transform=fig.transFigure)
    plt.text(Nxloc[idx],0.8,  dataset['label'] + r" $N_{off} = $"    +str(len(shouldPassQuantity))      , ha='left', size='x-small', color='cadetblue', transform=fig.transFigure)

plt.xlabel(vardict["xlabel"])
plt.ylabel("Trigger Efficiency")
plt.ylim(-0.06,1.2)
hep.cms.text("Preliminary")
hep.cms.lumitext(r"Summer23 (L=12.98 fb$^{-1}$)")
if analysis in ["LeadJetPtAnalysis", "SubleadJetPtAnalysis", "MjjAnalysis", "DetaAnalysis"]: plt.axvline(x=vardict["threshold"], color='seagreen', label="Threshold", linestyle="--")

line1 = r"$\geq 1$ tight $\mu$ ($p_T\geq 27$ GeV), IsoMu24, "
line2 = r"$>1$ ak4 jets, "
line3, line4 = "", ""
if analysis!="LeadJetPtAnalysis":    line3 += r"$p_{T1} > $" + str(triggerdict['leadjetpt']) + ", "
if analysis!="SubleadJetPtAnalysis": line3 += r"$p_{T2} > $" + str(triggerdict['subleadjetpt']) + ", "
if analysis!="MjjAnalysis":          line4 += r"$M_{jj} > $" + str(triggerdict['mjj']) + " GeV, "
if analysis!="DetaAnalysis":         line4 += r"$\Delta\eta(j1,j2) > $" + str(triggerdict['deta']) + ", "
plt.text(0.15, 0.65, line1, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.text(0.15, 0.62, line2, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.text(0.15, 0.59, line3, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.text(0.15, 0.56, line4, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.legend(loc=2)
plt.grid()

pltname_tight, pltname_fb = "", ""
if TightCuts : pltname_tight = "tight"
if filterbits: pltname_fb    = "wfb" # With Filter Bits
plt.savefig(f"{pltPath}{vardict['plotname']}_{pltname_tight}{pltname_fb}.png")
print(f"Efficiency plots made! Name: {pltPath}{vardict['plotname']}_{pltname_tight}{pltname_fb}.png")


### SHAPES ###
if shapeAnalysis:
    xlim, binsize, cands, passd = vardict["maxbin"], vardict["binsize"], vardict["HLTCandQuantity"], vardict["HLTPassedQuantity"]
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
    shapecount = 0
    cutyloc = [0.65,0.6,0.55,0.5]
    if analysis!="LeadJetPtAnalysis":
        plt.text(0.2, cutyloc[shapecount], f"leadptcut: {triggerdict['leadjetpt']}"      , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
        shapecount += 1
    if analysis!="SubleadJetPtAnalysis":
        plt.text(0.2, cutyloc[shapecount] , f"subleadptcut: {triggerdict['subleadjetpt']}", ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
        shapecount += 1
    if analysis!="MjjAnalysis":
        plt.text(0.2, cutyloc[shapecount], f"mjjcut: {triggerdict['mjj']}"               , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
        shapecount += 1
    if analysis!="DetaAnalysis":
        plt.text(0.2, cutyloc[shapecount] , f"detacut: {triggerdict['deta']}"             , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
        shapecount += 1
    if analysis in ["LeadJetPtAnalysis", "SubleadJetPtAnalysis", "MjjAnalysis", "DetaAnalysis"]:
        plt.axvline(x=vardict["threshold"], color='tab:red', label="Threshold", linestyle="--")
    plt.text(0.85,0.84, r"$N_{off/HLT} = $"+str(len(passd)), ha='right', size='x-small', color='cadetblue', transform=fig.transFigure)
    plt.text(0.85,0.8, r"$N_{off} = $"+str(len(cands)), ha='right', size='x-small', color='cadetblue', transform=fig.transFigure)
    plt.legend(loc='upper left')
    plt.grid()
    plt.savefig(f"{pltPath}{analysis[:-8]}_{pltname_tight}{pltname_fb}Shape.png")
    print(f"Shape plots made! Name: {pltPath}{analysis[:-8]}_{pltname_tight}{pltname_fb}Shape.png")