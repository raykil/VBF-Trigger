import mplhep as hep
import matplotlib.pyplot as plt
from optparse import OptionParser
import definitions as vbf
import json
import glob
import os

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
jsonpath    = options.jsonpath # "/eos/user/j/jkil/SUEP/vbftrigger/datasets/json/"
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
    #tight = glob.glob(f"{jsonpath}*fb*/*{analysis}*{triggerpath}*tight*.json") # outputs strings
    tight = sum([glob.glob(f"{jsonpath}{t}/*{analysis}*{triggerpath}*tight*") for t in os.listdir(jsonpath) if "prom" in t and "fb" not in t], [])
    #loose = glob.glob(f"{jsonpath}*fb*/*{analysis}*{triggerpath}*loose*.json")
    loose = sum([glob.glob(f"{jsonpath}{l}/*{analysis}*{triggerpath}*loose*") for l in os.listdir(jsonpath) if "prom" in l and "fb" not in l], [])
    #tight = glob.glob(f"{jsonpath}*C0v3fb*/*{analysis}*{triggerpath}*tight*.json") # subset, fixed
    #loose = glob.glob(f"{jsonpath}*C0v3fb*/*{analysis}*{triggerpath}*loose*.json")
    # later do this too and compare
    #tight = glob.glob(f"{jsonpath}*C0v3fb*/*{analysis}*{triggerpath}*tight.json") # subset but original
    #loose = glob.glob(f"{jsonpath}*C0v3fb*/*{analysis}*{triggerpath}*loose.json")
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
    if   compare=="tt"     : vardicts = [tight_vardict, loose_vardict]
    elif tightcuts=="tight": vardicts = [tight_vardict]
    elif tightcuts=="loose": vardicts = [loose_vardict]

print("dataset loaded! Moving on to plotting...")
plt.style.use(hep.style.CMS)
fig = plt.figure()
for vardict in vardicts:
    effs, yerrmin, yerrmax, bincenters = vbf.GetEfficiency(vardict["binsize"], vardict["maxbin"], vardict["numerator"], vardict["denominator"])
    plt.errorbar(bincenters, effs, yerr=[yerrmin,yerrmax], xerr=vardict["binsize"], marker='o', color=vardict["color"], label=f"{vardict['label']} Efficiency", linestyle='')
    if effoutdir: 
        effdict = vbf.GetEffDict(vardict, trigdict, effs, yerrmin, yerrmax, bincenters)
        with open(f"{effoutdir}{analysis}_{triggerpath}_{compare}_{vardict['label']}_effvals.json", 'w') as j: json.dump(effdict, j, cls=vbf.NpEncoder, indent=4)

#plt.text(0.6,0.84, r" $N_{off/HLT} = $"+str(len(vardict["numerator"]))  , ha='left', size='x-small', color='cadetblue', transform=fig.transFigure)
#plt.text(0.6,0.8,  r" $N_{off} = $"    +str(len(vardict["denominator"])), ha='left', size='x-small', color='cadetblue', transform=fig.transFigure)
plt.xlabel(vardict["xlabel"])
plt.ylabel("Trigger Efficiency")
plt.ylim(-0.06,1.2)
hep.cms.text("Preliminary")
hep.cms.lumitext(r"$L=21.70 \,fb^{-1}$ 2023 (13.6 TeV)")
if analysis in ["leadpt", "subleadpt", "mjj", "deta"]: plt.axvline(x=vardict["threshold"], color='red', label="Threshold", linestyle="--")

line1 = r"$\geq 1$ tight $\mu$ ($p_T\geq 27$ GeV), IsoMu24, "
line2 = r"$\geq 2$ ak4 jets, "
line3, line4 = "", ""
if analysis!="leadpt"   : line3 += r"$p_{T1} > $" + str(trigdict['leadjetpt']) + ", "
if analysis!="subleadpt": line3 += r"$p_{T2} > $" + str(trigdict['subleadjetpt']) + ", "
if analysis!="mjj"      : line4 += r"$M_{jj} > $" + str(trigdict['mjj']) + " GeV, "
if analysis!="deta"     : line4 += r"$\Delta\eta(j1,j2) > $" + str(trigdict['deta']) + ", "
plt.text(0.45, 0.30, line1, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.text(0.45, 0.27, line2, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.text(0.45, 0.24, line3, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.text(0.45, 0.21, line4, ha='left', size='x-small', color='darkslategray', transform=fig.transFigure)
plt.legend(loc=2)
plt.grid()

plt.savefig(f"{outputdir}{analysis}_{triggerpath}{'_'+compare}{tightcuts}.png")
print(      f"{outputdir}{analysis}_{triggerpath}{'_'+compare}{tightcuts}.png made!")