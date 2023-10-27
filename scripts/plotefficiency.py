import os, json, glob
import numpy as np
import mplhep as hep
import definitions as vbf
import matplotlib.pyplot as plt
from optparse import OptionParser

parser = OptionParser(usage="%prog [options]")
parser.add_option("--triggerpath", dest="triggerpath", default="pt105" , help="if comparing, we can leave out the triggerpath. If single plotting, you must specify the triggerpath.")
parser.add_option("--analysis"   , dest="analysis"   , default="leadpt", help="options: LeadJetPtAnalysis, SubleadJetPtAnalysis, MjjAnalysis, DetaAnalysis")
parser.add_option("--tightcuts"  , dest="tightcuts"  , default=""      , help="put 'tight' of 'loose'. If compare=tt, then doesn't matter.")
parser.add_option("--outputdir"  , dest="outputdir"  , default="./"    , help="plot output directory")
parser.add_option("--effoutdir"  , dest="effoutdir"  , default=""      , help="efficiency plot values output directory. If not wanted, leave void.")
parser.add_option("--shape"      , dest="shape"      , default=False   , help="produce histograms of property distribution")
parser.add_option("--jsonpath"   , dest="jsonpath"   , default="./"    , help="directory where the quantity json files are.")
parser.add_option("--compare"    , dest="compare"    , default=""      , help="If void, it does not compare anything (all dataset into one quantity). pp=prompt vs parking, cd=dataset c vs d, tt=tight vs not")
(options, args) = parser.parse_args()

triggerpath = options.triggerpath
analysis    = options.analysis
tightcuts   = options.tightcuts
outputdir   = options.outputdir
effoutdir   = options.effoutdir
shape       = options.shape
jsonpath    = options.jsonpath
compare     = options.compare

# sorting out datasets
trigdict = vbf.GetTriggerDict(triggerpath, analysis, tightcuts)
if   compare=="pp":
    #prom = 
    #park = 
    pass
elif compare=="cd":
    #c = 
    #d = 
    pass
else:
    tight = sum([glob.glob(f"{jsonpath}{t}/*{analysis}*{triggerpath}*tight*") for t in os.listdir(jsonpath) if "prom" in t and "fb" not in t], []) # not in 
    loose = sum([glob.glob(f"{jsonpath}{l}/*{analysis}*{triggerpath}*loose*") for l in os.listdir(jsonpath) if "prom" in l and "fb" not in l], []) # not in 
    tight_numerators, tight_denominators, loose_numerators, loose_denominators = [],[],[],[]

    for t, l in zip(tight, loose):
        tights, looses = json.load(open(t,'r')), json.load(open(l,'r'))
        tight_numerators.extend(tights["numerator"])
        tight_denominators.extend(tights["denominator"])
        loose_numerators.extend(looses["numerator"])
        loose_denominators.extend(looses["denominator"])
    tight_vardict = vbf.GetVardict(tight_numerators, tight_denominators, analysis, trigdict)
    loose_vardict = vbf.GetVardict(loose_numerators, loose_denominators, analysis, trigdict)
    tight_vardict.update({"label": "tight", "color": 'b'})
    loose_vardict.update({"label": "loose", "color": 'r'})
    if   compare=="tl"     : vardicts = [tight_vardict, loose_vardict]
    elif tightcuts=="tight": vardicts = [tight_vardict]
    elif tightcuts=="loose": vardicts = [loose_vardict]

print("dataset loaded! Moving on to plotting...")

### EFFICIENCY ###
plt.style.use(hep.style.CMS)
fig = plt.figure()
for vardict in vardicts:
    effs, yerrmin, yerrmax, bincenters = vbf.GetEfficiency(vardict["binsize"], vardict["maxbin"], vardict["numerator"], vardict["denominator"])
    plt.errorbar(bincenters, effs, yerr=[yerrmin,yerrmax], xerr=vardict["binsize"], marker='o', color=vardict["color"], label=f"HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5(_TripleJet) Efficiency ({vardict['label']})", linestyle='')
    if effoutdir: 
        effdict = vbf.GetEffDict(vardict, trigdict, effs, yerrmin, yerrmax, bincenters)
        with open(f"{effoutdir}{analysis}_{triggerpath}_{compare}_{vardict['label']}_effvals.json", 'w') as j: json.dump(effdict, j, cls=vbf.NpEncoder, indent=4)

plt.xlabel(vardict["xlabel"])
plt.ylabel("Trigger Efficiency")
plt.ylim(-0.05,1.1)
hep.cms.text("Preliminary")
hep.cms.lumitext(r"$L=21.70 \,fb^{-1}$ 2023 (13.6 TeV)")
if analysis in ["leadpt", "subleadpt", "mjj", "deta"]: plt.axvline(x=vardict["threshold"], color='g', label="Threshold", linestyle="--")

line1 = r"$\geq 1$ tight $\mu$ ($p_T\geq 27$ GeV), IsoMu24, "
line2 = r"$\geq 2$ ak4 jets, "
line3, line4 = "", ""
if analysis!="leadpt"   : line3 += r"$p_{T1} > $" + str(trigdict['leadjetpt']) + ", "
if analysis!="subleadpt": line3 += r"$p_{T2} > $" + str(trigdict['subleadjetpt']) + ", "
if analysis!="mjj"      : line4 += r"$M_{jj} > $" + str(trigdict['mjj']) + " GeV, "
if analysis!="deta"     : line4 += r"$\Delta\eta(j1,j2) > $" + str(trigdict['deta']) + ", "
plt.text(0.48, 0.30, line1, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.text(0.48, 0.27, line2, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.text(0.48, 0.24, line3, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.text(0.48, 0.21, line4, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.legend(loc=2, fontsize='15')
plt.grid()

plt.savefig(f"{outputdir}{analysis}_{triggerpath}{'_'+compare}{tightcuts}.png")
print(f"{outputdir}{analysis}_{triggerpath}{'_'+compare}{tightcuts}.png made!")

### SHAPE ###
if shape:
    plt.style.use(hep.style.CMS)
    fig = plt.figure()
    xlim , binsize = vardict["maxbin"], vardict["binsize"]
    denom, num     = vardict["denominator"], vardict["numerator"]
    denomHist, denomBins = np.histogram(denom, bins=np.arange(0,xlim+binsize,binsize))
    numHist  , numBins   = np.histogram(num  , bins=np.arange(0,xlim+binsize,binsize))
    hep.histplot(denomHist, denomBins, histtype='step', label=f"denom {analysis[:-8]}", color="tab:blue"  , density=False, stack=True)
    hep.histplot(numHist  , numBins  , histtype='step', label=f"num {analysis[:-8]}"  , color="tab:orange", density=False, stack=True, linestyle='--')
    hep.cms.text("Preliminary")
    hep.cms.lumitext(r"$L=21.70 \,fb^{-1}$ 2023 (13.6 TeV)")
    plt.xlabel(vardict["xlabel"])
    plt.ylabel("Counts")
    plt.text(0.15,0.82, r" $N_{off/HLT} = $"+str(len(vardict["numerator"]))  , ha='left', size='x-small', color='cadetblue', transform=fig.transFigure)
    plt.text(0.15,0.78,  r" $N_{off} = $"   +str(len(vardict["denominator"])), ha='left', size='x-small', color='cadetblue', transform=fig.transFigure)
    line1 = r"$\geq 1$ tight $\mu$ ($p_T\geq 27$ GeV), IsoMu24, "
    line2 = r"$\geq 2$ ak4 jets, "
    line3, line4 = "", ""
    if analysis!="leadpt"   : line3 += r"$p_{T1} > $" + str(trigdict['leadjetpt']) + ", "
    if analysis!="subleadpt": line3 += r"$p_{T2} > $" + str(trigdict['subleadjetpt']) + ", "
    if analysis!="mjj"      : line4 += r"$M_{jj} > $" + str(trigdict['mjj']) + " GeV, "
    if analysis!="deta"     : line4 += r"$\Delta\eta(j1,j2) > $" + str(trigdict['deta']) + ", "
    plt.text(0.48, 0.68, line1, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
    plt.text(0.48, 0.65, line2, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
    plt.text(0.48, 0.62, line3, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
    plt.text(0.48, 0.59, line4, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
    if analysis in ["leadpt", "subleadpt", "mjj", "deta"]: plt.axvline(x=vardict["threshold"], color='g', label="Threshold", linestyle="--")
    plt.legend(loc='upper right')
    plt.grid()
    plt.savefig(f"{outputdir}{analysis}_{triggerpath}{'_'+compare}{tightcuts}_shape.png")
    print(f"{outputdir}{analysis}_{triggerpath}{'_'+compare}{tightcuts}_shape.png made!")