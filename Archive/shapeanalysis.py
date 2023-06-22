import numpy as np
import awkward as ak
import uproot
import vector
import os
import mplhep as hep
import matplotlib.pyplot as plt

def ApplyCuts(Jets):
    ptCut      = (Jets.pt>20)
    Jets = Jets[ptCut]
    
    nTracksCut = (Jets.nTracks>20)
    Jets = Jets[nTracksCut]

    nJetCut    = (ak.num(Jets)>=2) # This is event-wise cut.
    Jets = Jets[nJetCut]
    return Jets


def GetMaxMjj(Jets):
    JetCombo = ak.combinations(Jets,2, fields=["jet1","jet2"])
    jjCombo  = JetCombo.jet1 + JetCombo.jet2

    # negative value troubleshooting
    mjjCombo2 = (jjCombo.E)**2 - (jjCombo.px**2 + jjCombo.py**2 + jjCombo.pz**2)
    negativecut = (mjjCombo2<0)
    negCombo = mjjCombo2[negativecut]
    print("anomalous events: ", len(ak.flatten(negCombo)))

    mjjCombo = np.sqrt(np.abs((jjCombo.E)**2 - (jjCombo.px**2 + jjCombo.py**2 + jjCombo.pz**2)))
    maxmjj   = ak.max(mjjCombo,axis=1)
    return maxmjj

### LOADING SAMPLES ###
# Convert root files in one directory into an ak array
sigPath = "/eos/user/j/jkil/SUEP/suep-production/signals/UL18/VBFpythia_generic_new_M125_MD2_T2_HT-1_/NANOAOD/" # These directories contain multiple files!
ewkPath = "/eos/user/j/jkil/SUEP/suep-production/backgrounds/EWKW/Wminus2Jets/"
qcdPath = "/eos/home-j/jkil/SUEP/suep-production/backgrounds/QCD/inclusive/"

sigFileNames, ewkFileNames, qcdFileNames = os.listdir(sigPath)[:2], os.listdir(ewkPath)[:2], os.listdir(qcdPath)[:2]
sigMaxMjjs,   ewkMaxMjjs,   qcdMaxMjjs   = [],[],[]

"""
print("Starting sig analysis!")
for filename in sigFileNames:
    print("processing file {}".format(filename))
    f      = uproot.open(sigPath+filename)
    events = f["Events"]

    Jets = vector.zip({
    "pt"  : events["Jet_pt"].array(),
    "eta" : events["Jet_eta"].array(),
    "phi" : events["Jet_phi"].array(), 
    "mass": events["Jet_mass"].array(),
    "nTracks": events["Jet_nConstituents"].array()
    })
    
    Jets = ApplyCuts(Jets)
    maxmjj     = GetMaxMjj(Jets)
    sigMaxMjjs = np.concatenate((sigMaxMjjs,maxmjj))
    sigMaxMjjs = sigMaxMjjs[np.isfinite(sigMaxMjjs)]

print("\n")
print("Starting ewk analysis!")
for filename in ewkFileNames:
    print("processing file {}".format(filename))
    f = uproot.open(ewkPath+filename)
    events = f["Events"]
    
    Jets = vector.zip({
    "pt"  : events["Jet_pt"].array(),
    "eta" : events["Jet_eta"].array(),
    "phi" : events["Jet_phi"].array(), 
    "mass": events["Jet_mass"].array(),
    "nTracks": events["Jet_nConstituents"].array()
    })

    Jets = ApplyCuts(Jets)
    maxmjj     = GetMaxMjj(Jets)
    ewkMaxMjjs = np.concatenate((ewkMaxMjjs,maxmjj))
    ewkMaxMjjs = ewkMaxMjjs[np.isfinite(ewkMaxMjjs)]
"""

print("\n")
print("Starting qcd analysis!")
for filename in qcdFileNames:
    print("processing file {}".format(filename))
    f = uproot.open(qcdPath+filename)
    events = f["Events"]
    
    Jets = vector.zip({
    "pt"  : events["Jet_pt"].array(),
    "eta" : events["Jet_eta"].array(),
    "phi" : events["Jet_phi"].array(), 
    "mass": events["Jet_mass"].array(),
    "nTracks": events["Jet_nConstituents"].array(),
    "genWeight": events["genWeight"].array()
    })

    Jets = ApplyCuts(Jets)
    maxmjj     = GetMaxMjj(Jets)
    qcdMaxMjjs = np.concatenate((qcdMaxMjjs,maxmjj))
    qcdMaxMjjs = qcdMaxMjjs[np.isfinite(qcdMaxMjjs)]



print("\n")
print("Starting the plots!")
pltPath = "/eos/user/j/jkil/www/VBFSUEP/shapeAnalysis/"
xlim = 4000
binsize = 200
#sighist, sigbins = np.histogram(sigMaxMjjs, bins=np.arange(min(sigMaxMjjs), max(sigMaxMjjs) + binsize, binsize))
#ewkhist, ewkbins = np.histogram(ewkMaxMjjs, bins=np.arange(min(ewkMaxMjjs), max(ewkMaxMjjs) + binsize, binsize))
sighist, sigbins = np.histogram(sigMaxMjjs, bins=50)
ewkhist, ewkbins = np.histogram(ewkMaxMjjs, bins=50)
qcdhist, qcdbins = np.histogram(qcdMaxMjjs, bins=50)
#qcdhist, qcdbins = np.histogram(qcdMaxMjjs, bins=int((max(qcdMaxMjjs) - min(qcdMaxMjjs)) / binsize))
plt.style.use(hep.style.CMS)
plt.figure()
#hep.histplot(sighist, sigbins, histtype='step', label='signal',        color='tab:blue',   density=True, stack=True)
#hep.histplot(ewkhist, ewkbins, histtype='step', label='EWKW',          color='tab:green',  density=True, stack=True)
hep.histplot(qcdhist, qcdbins, histtype='step', label='QCD Inclusive', color='tab:orange', density=True, stack=True, weights=Jets.genWeight[:,0])
hep.cms.text("Simulation")
hep.cms.lumitext(r"UL18, (13 TeV)")
plt.xlabel(r"$m_{jj}^{max}$ (GeV)")
plt.ylabel(r"Normalized Counts")
plt.xlim(0,xlim)
plt.legend()
plt.savefig("{}shape.png".format(pltPath))