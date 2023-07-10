import awkward as ak
import vector
import mplhep as hep
import matplotlib.pyplot as plt
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
from scipy.stats import beta
import definitions as vbf

### PREPROCESSING ###
parser.add_option("--whichfiles" , dest="whichfiles" , default="singlemuon"                           , help="options: singlemuon, zerobias")
parser.add_option("--triggerpath", dest="triggerpath", default="pt105Analysis"                        , help="options: pt105Analysis, pt125Analysis")
parser.add_option("--analysis"   , dest="analysis"   , default="LeadJetPtAnalysis"                    , help="options: LeadJetPtAnalysis, SubleadJetPtAnalysis, MjjAnalysis, DetaAnalysis")
parser.add_option("--tightcuts"  , dest="tightcuts"  , default=False                                  , help="options: True, False")
parser.add_option("--outputdir"  , dest="outputdir"  , default="/Users/raymondkil/Desktop/vbftrigger/" , help="output directory")
(options, args) = parser.parse_args()

whichfiles  = options.whichfiles
triggerpath = options.triggerpath
analysis    = options.analysis
TightCuts   = options.tightcuts
outputdir   = options.outputdir

if whichfiles=="singlemuon":
    #path = "/eos/user/j/jkil/SUEP/suep-production/summer23data/singlemuon/"
    path = "/Users/raymondkil/Desktop/vbftrigger/run3parquets/"
    #path = "/eos/user/j/jkil/SUEP/suep-production/run3parquets/"
    datasetname = "SingleMuon"
    OFFJets = ak.from_parquet(path + "run3singlemuon_OFFJets*")
    HLTJets = ak.from_parquet(path + "run3singlemuon_HLTJets*")
    MuonCollections = ak.from_parquet(path + "run3singlemuon_MuonCollections*")
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
    print("Successfully loaded objects using parquet! len: {0}".format(len(OFFJets)))
if whichfiles=="zerobias":
    path = "/eos/user/j/jkil/SUEP/suep-production/summer23data/zerobias/"
    datasetname = "ZeroBias"

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

OFFJets, HLTJets, MuonCollections = vbf.ApplyBasicCuts(OFFJets, HLTJets, MuonCollections, analysis)
cleanOFFJets, cleanHLTJets, cleanMuonCollections, cleanOFFcombo = vbf.ApplyTriggerCuts(OFFJets, HLTJets, MuonCollections, analysis, triggerdict)
shouldPassHLT_Jets, shouldPassHLT_MaxMjjCombo = vbf.SelectHLTPassedJets(cleanOFFJets, cleanOFFcombo)

if   triggerpath=="pt105Analysis": HLTpassedJets = shouldPassHLT_Jets[cleanHLTJets.pt105|cleanHLTJets.pt105triple]
elif triggerpath=="pt125Analysis": HLTpassedJets = shouldPassHLT_Jets[cleanHLTJets.pt125|cleanHLTJets.pt125triple]

print("\n")
print("Number of events that passed HLT: {}".format(len(HLTpassedJets)))
print("Number of offline events: {}".format(len(shouldPassHLT_Jets)))

### POSTPROCESSING ###
if analysis=="LeadJetPtAnalysis":
    vardict = {
        "plotname": "leadpt",
        "binsize"  : 5,
        "HLTPassedQuantity": HLTpassedJets.pt[:,0],
        "OFFJetQuantity": shouldPassHLT_Jets.pt[:,0],
        "maxbin": 250,
        "xlabel": r"Offline $p_T^{leadjet}$ (GeV)",
        "threshold": triggerdict["leadjetpt"],
    }

if analysis=="SubleadJetPtAnalysis":
    vardict = {
        "plotname": "subleadpt",
        "binsize"  : 2,
        "HLTPassedQuantity": HLTpassedJets.pt[:,1],
        "OFFJetQuantity": shouldPassHLT_Jets.pt[:,1],
        "maxbin": 100,
        "xlabel": r"Offline $p_T^{subleadjet}$ (GeV)",
        "threshold": triggerdict["subleadjetpt"],
    }

if analysis=="MjjAnalysis":
    vardict = {
        "plotname": "mjj",
        "binsize"  : 50,
        "HLTPassedQuantity": vbf.GetMaxMjj(HLTpassedJets)[0],
        "OFFJetQuantity": vbf.GetMaxMjj(shouldPassHLT_Jets)[0],
        "maxbin": 2500,
        "xlabel": r"Offline $M_{jj}$ (GeV)",
        "threshold": triggerdict["mjj"],
    }

if analysis=="DetaAnalysis":
    vardict = {
        "plotname": "deta",
        "binsize"  : 0.1,
        "HLTPassedQuantity": vbf.GetMaxEta(HLTpassedJets),
        "OFFJetQuantity": vbf.GetMaxEta(shouldPassHLT_Jets),
        "maxbin": 8,
        "xlabel": r"Offline $\Delta\eta$",
        "threshold": triggerdict["deta"],
    }

# JetID analysis requires jet-wise efficiency calculation...in progress
# Need more attention from this point on!

# leadjet
if analysis=="LeadJetchEmEFAnalysis":
    vardict = {
        "plotname": "LeadJetchEmEF",
        "binsize"  : 0.025,
        "HLTPassedQuantity": HLTpassedJets.chEmEF[:,0],
        "OFFJetQuantity": shouldPassHLT_Jets.chEmEF[:,0],
        "maxbin": 1.0,
        "xlabel": "Leadjet chEmEF",
        "threshold": -999,
    }

if analysis=="LeadJetchHEFAnalysis":
    vardict = {
        "plotname": "LeadJetchHEF",
        "binsize"  : 0.025,
        "HLTPassedQuantity": HLTpassedJets.chHEF[:,0],
        "OFFJetQuantity": shouldPassHLT_Jets.chHEF[:,0],
        "maxbin": 1.0, # Should make bin to exceed 1, because in eff calc, I am binning the events so that quantity < maxbin, which does not include 1, while there are events with EF==1.
        "xlabel": "Leadjet chHEF",
        "threshold": -999,
    }

if analysis=="LeadJetneEmEFAnalysis":
    vardict = {
        "plotname": "LeadJetneEmEF",
        "binsize"  : 0.025,
        "HLTPassedQuantity": HLTpassedJets.neEmEF[:,0],
        "OFFJetQuantity": shouldPassHLT_Jets.neEmEF[:,0],
        "maxbin": 1.0,
        "xlabel": "Leadjet neEmEF",
        "threshold": -999,
    }

if analysis=="LeadJetneHEFAnalysis":
    vardict = {
        "plotname": "LeadJetneHEF",
        "binsize"  : 0.025,
        "HLTPassedQuantity": HLTpassedJets.neHEF[:,0],
        "OFFJetQuantity": shouldPassHLT_Jets.neHEF[:,0],
        "maxbin": 1.0,
        "xlabel": "Leadjet neHEF",
        "threshold": -999,
    }

if analysis=="LeadJetmuEFAnalysis":
    vardict = {
        "plotname": "LeadJetmuEF",
        "binsize"  : 0.025,
        "HLTPassedQuantity": HLTpassedJets.muEF[:,0],
        "OFFJetQuantity": shouldPassHLT_Jets.muEF[:,0],
        "maxbin": 1.0,
        "xlabel": "Leadjet muEF",
        "threshold": -999,
    }

#subleadjet 
if analysis=="SubLeadJetchEmEFAnalysis":
    vardict = {
        "plotname": "SubLeadJetchEmEF",
        "binsize"  : 0.025,
        "HLTPassedQuantity": HLTpassedJets.chEmEF[:,1],
        "OFFJetQuantity": shouldPassHLT_Jets.chEmEF[:,1],
        "maxbin": 1.0,
        "xlabel": "SubLeadJet chEmEF",
        "threshold": -999,
    }

if analysis=="SubLeadJetchHEFAnalysis":
    vardict = {
        "plotname": "SubLeadJetchHEF",
        "binsize"  : 0.025,
        "HLTPassedQuantity": HLTpassedJets.chHEF[:,1],
        "OFFJetQuantity": shouldPassHLT_Jets.chHEF[:,1],
        "maxbin": 1.0, # Should make bin to exceed 1, because in eff calc, I am binning the events so that quantity < maxbin, which does not include 1, while there are events with EF==1.
        "xlabel": "SubLeadJet chHEF",
        "threshold": -999,
    }

if analysis=="SubLeadJetneEmEFAnalysis":
    vardict = {
        "plotname": "SubLeadJetneEmEF",
        "binsize"  : 0.025,
        "HLTPassedQuantity": HLTpassedJets.neEmEF[:,1],
        "OFFJetQuantity": shouldPassHLT_Jets.neEmEF[:,1],
        "maxbin": 1.0,
        "xlabel": "SubLeadJet neEmEF",
        "threshold": -999,
    }

if analysis=="SubLeadJetneHEFAnalysis":
    vardict = {
        "plotname": "SubLeadJetneHEF",
        "binsize"  : 0.025,
        "HLTPassedQuantity": HLTpassedJets.neHEF[:,1],
        "OFFJetQuantity": shouldPassHLT_Jets.neHEF[:,1],
        "maxbin": 1.0,
        "xlabel": "SubLeadJet neHEF",
        "threshold": -999,
    }

if analysis=="SubLeadJetmuEFAnalysis":
    vardict = {
        "plotname": "SubLeadJetmuEF",
        "binsize"  : 0.025,
        "HLTPassedQuantity": HLTpassedJets.muEF[:,1],
        "OFFJetQuantity": shouldPassHLT_Jets.muEF[:,1],
        "maxbin": 1.0,
        "xlabel": "SubLeadJet muEF",
        "threshold": -999,
    }

### EFFICIENCY ###
effs, yerrmin, yerrmax, bincenters = vbf.GetEfficiency(vardict["binsize"], vardict["maxbin"], vardict["HLTPassedQuantity"], vardict["OFFJetQuantity"])


### PLOTTING ###
#pltPath = "/eos/user/j/jkil/www/VBFSUEP/efficiency/combo_allfiles/"
pltPath = outputdir
plt.style.use(hep.style.CMS)
fig = plt.figure()

plt.errorbar(bincenters,effs, yerr=[yerrmin,yerrmax], xerr=vardict["binsize"], marker='o', color="black", label="Efficiency", linestyle='')
plt.xlabel(vardict["xlabel"])
plt.ylabel("Efficiency")
plt.ylim(-0.06,1.2)
hep.cms.text("Preliminary")
hep.cms.lumitext(r"Summer23 (L=1.01 fb$^{-1}$)")
if analysis in ["LeadJetPtAnalysis", "SubleadJetPtAnalysis", "MjjAnalysis", "DetaAnalysis"]:
    plt.axvline(x=vardict["threshold"], color='tab:red', label="Threshold", linestyle="--")

plt.text(0,1.0,"dataset: {}".format(datasetname), size='x-small', color='steelblue')
plt.text(0.2, 0.75,r"$\geq 1$ tight $\mu$ ($p_T\geq 27$ GeV), pass HLT_IsoMu24", ha='left', va='top', size='x-small', color='red', transform=fig.transFigure)
if analysis!="LeadJetPtAnalysis":    plt.text(0.2, 0.65, "leadptcut: {}".format(triggerdict["leadjetpt"])      , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
if analysis!="SubleadJetPtAnalysis": plt.text(0.2, 0.6 , "subleadptcut: {}".format(triggerdict["subleadjetpt"]), ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
if analysis!="MjjAnalysis":          plt.text(0.2, 0.55, "mjjcut: {}".format(triggerdict["mjj"])               , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)
if analysis!="DetaAnalysis":         plt.text(0.2, 0.5 , "detacut: {}".format(triggerdict["deta"])             , ha='left', size='x-small', color='steelblue', transform=fig.transFigure)

plt.text(0.85,0.84, r"$N_{off/HLT} = $"+str(len(HLTpassedJets)), ha='right', size='x-small', color='cadetblue', transform=fig.transFigure)
plt.text(0.85,0.8, r"$N_{off} = $"+str(len(shouldPassHLT_Jets)), ha='right', size='x-small', color='cadetblue', transform=fig.transFigure)

plt.legend(loc=2)
plt.grid()
if TightCuts:
    plt.savefig("{0}{1}_Tight.png".format(pltPath,vardict["plotname"]))
    print("Plots made! Name: {0}{1}_TightEff.png".format(pltPath,vardict["plotname"]))
else:
    plt.savefig("{0}{1}.png".format(pltPath,vardict["plotname"]))
    print("Plots made! Name: {0}{1}_Eff.png".format(pltPath,vardict["plotname"]))
