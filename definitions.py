import numpy as np
import awkward as ak
import uproot
import vector
from scipy.stats import beta

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

    # This cut is now passing an event if it has at least one (reasonably, i.e., muRelIso<0.2) isolated muon 
    MuonCuts = (ak.any((MuonCollections.Muon_pt>=27) & (MuonCollections.muRelIso<0.2), axis=1))
    OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, MuonCuts)
    print("number of events after MuonCuts: {}".format(len(OFFJets)))

    IsoMu24Cut = HLTJets.IsoMu24
    OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, IsoMu24Cut)
    print("number of events after IsoMu24Cut: {}".format(len(OFFJets)))

    return OFFJets, HLTJets, MuonCollections

"""
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
"""

def ApplyTriggerCuts(OFFJets, HLTJets, MuonCollections, analysis, triggerdict):
    OFFcombo = ak.combinations(OFFJets,2, fields=["jet1","jet2"])
    #print("number of events before cuts: ", ak.count_nonzero(OFFcombo))
    print("number of jet pairs before cuts: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="LeadJetPtAnalysis":
        leadjetptcut = (OFFcombo.jet1.pt>=triggerdict["leadjetpt"])
        OFFcombo = OFFcombo[leadjetptcut]
        #print("number of events after leadjetptcut: ", ak.count_nonzero(OFFcombo))
        print("number of jet pairs after leadjetptcut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="SubleadJetPtAnalysis":
        subleadjetptcut = (OFFcombo.jet2.pt>=triggerdict["subleadjetpt"])
        OFFcombo = OFFcombo[subleadjetptcut]
        #print("number of events after subleadjetptcut: ", ak.count_nonzero(OFFcombo))
        print("number of jet pairs after subleadjetptcut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="MjjAnalysis":
        jjsum  = OFFcombo.jet1 + OFFcombo.jet2
        mjjcut = (jjsum.mass>=triggerdict["mjj"])
        OFFcombo = OFFcombo[mjjcut]
        #print("number of events after mjjcut: ", ak.count_nonzero(OFFcombo))
        print("number of jet pairs after mjjcut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="DetaAnalysis":
        detacut = (vector.Spatial.deltaeta(OFFcombo.jet1, OFFcombo.jet2) >= triggerdict["deta"])
        OFFcombo = OFFcombo[detacut]
        #print("number of events after detacut: ", ak.count_nonzero(OFFcombo))
        print("number of jet pairs after detacut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    eventcut = ak.where(ak.num(OFFcombo)>0,True, False)
    OFFcombo = OFFcombo[eventcut]
    OFFJets = OFFJets[eventcut]
    HLTJets = HLTJets[eventcut]
    MuonCollections = MuonCollections[eventcut] # Do we need this?
    print("number of survived events: ", len(OFFJets))

    return OFFJets, HLTJets, MuonCollections, OFFcombo

def SelectHLTPassedJets(Jets, OFFcombo): # OFFcombo from ApplyTriggerCuts!!!
    exp_OFFcombo_jet1, exp_OFFJets_pt = ak.broadcast_arrays(OFFcombo.jet1, Jets.pt[:,np.newaxis], depth_limit=2)
    exp_OFFcombo_jet2, exp_OFFJets_pt = ak.broadcast_arrays(OFFcombo.jet2, Jets.pt[:,np.newaxis], depth_limit=2)
    jet1mask = ak.where(exp_OFFJets_pt==exp_OFFcombo_jet1.pt,True,False)
    jet2mask = ak.where(exp_OFFJets_pt==exp_OFFcombo_jet2.pt,True,False)

    padding_target = ak.max(ak.num(Jets.pt))
    cutbool = ak.fill_none(ak.pad_none(ak.where(Jets.pt!=-999,True,False),padding_target,axis=-1),False)
    padded_jet1mask, padded_jet2mask = ak.pad_none(jet1mask, padding_target, axis=1), ak.pad_none(jet2mask, padding_target, axis=1)
    padded_jet1mask, padded_jet2mask = ak.fill_none(padded_jet1mask,[False],axis=1), ak.fill_none(padded_jet2mask,[False],axis=1)

    padded_jet1mask, padded_jet2mask = ak.pad_none(padded_jet1mask,ak.max(ak.num(padded_jet1mask,axis=2)),axis=2), ak.pad_none(padded_jet2mask,ak.max(ak.num(padded_jet2mask,axis=2)),axis=2)

    padded_jet1mask, padded_jet2mask = ak.to_numpy(padded_jet1mask,allow_missing=True), ak.to_numpy(padded_jet2mask,allow_missing=True)
    swapped_jet1mask, swapped_jet2mask = np.swapaxes(padded_jet1mask,0,1), np.swapaxes(padded_jet2mask,0,1)
    swapped_jet1mask, swapped_jet2mask = ak.any(swapped_jet1mask,axis=0), ak.any(swapped_jet2mask,axis=0)

    jetmask = (swapped_jet1mask)|(swapped_jet2mask)
    jetmask = jetmask[cutbool]
    HLTPassedJets = Jets[jetmask]

    # for events that have multiple jet pairs that pass HLT trigger path, I'm now selecting the jet pair that creates maxmjj.
    j1, j2 = OFFcombo.jet1, OFFcombo.jet2
    jj = j1+j2
    argmaxmjj = ak.Array(ak.to_list(np.expand_dims(ak.argmax(jj.mass, axis=1),axis=1)))
    HLTPassed_MaxMjjCombo = OFFcombo[argmaxmjj]

    return HLTPassedJets, HLTPassed_MaxMjjCombo # retrieving maxmjjcombo: maxmjjcombo.jet1 gives leadjet, maxmjjcombo.jet2 gives subleadjet

def MakeObjects(filenames,path):
    OFFJets, HLTJets, MuonCollections = [],ak.Array([]), []
    for filename in filenames:
        print("Processing file {0}".format(filename))
        f = uproot.open(path + filename)
        events = f["Events"]

        HLTJet = ak.zip({ # Regular array corresponding to events...... Maybe change the name to HLTPath(s) for more intuition
            "pt105":       events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5"].array(),
            "pt105triple": events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5_TriplePFJet"].array(),
            "pt125":       events["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0"].array(),
            "pt125triple": events["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0_TriplePFJet"].array(),

            "IsoMu24": events["HLT_IsoMu24"].array(),
        })

        OFFJet = vector.zip({ # Jagged array with subarrays corresponding to jets
            "pt": events["Jet_pt"].array(),
            "eta": events["Jet_eta"].array(),
            "phi": events["Jet_phi"].array(),
            "mass": events["Jet_mass"].array(),
            "nTracks": events["Jet_nConstituents"].array(),

            "chEmEF": events["Jet_chEmEF"].array(),
            "chHEF": events["Jet_chHEF"].array(),
            "neEmEF": events["Jet_neEmEF"].array(),
            "neHEF": events["Jet_neHEF"].array(),
            "muEF": events["Jet_muEF"].array(),
        })

        MuonCollection = ak.zip({ # Jagged array with subarrays corresponding to muons
            "nMuon": events["nMuon"].array(),
            "Muon_pt": events["Muon_pt"].array(),
            "muRelIso": events["Muon_pfRelIso04_all"].array() # relative isolation of muons
        })

        OFFJets = ak.concatenate((OFFJets, OFFJet))
        HLTJets = ak.concatenate((HLTJets, HLTJet))
        MuonCollections = ak.concatenate((MuonCollections, MuonCollection))

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
        errmin[i],errmax[i] = clopper_pearson_interval(nHLT,nOFF,0.05)
        if nOFF!=0: effs[i] = nHLT/nOFF
    yerrmin, yerrmax = np.nan_to_num(errmin), np.nan_to_num(errmax)

    return effs, yerrmin, yerrmax, bincenters