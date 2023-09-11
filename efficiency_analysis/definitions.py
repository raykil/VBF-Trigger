"""
    This script contains the function definitions used in HLT VBF Trigger efficiency analysis for Run3 Summer2023 data.
    Raymond Kil, 2023
"""

import numpy as np
import awkward as ak
import uproot
import vector
from scipy.stats import beta
from time import time 

def MakeObjects(filenames,path):
    OFFJets, HLTJets, MuonCollections, TrigObjs = [],ak.Array([]), [], []
    for filename in filenames:
        print("Processing file {0}".format(filename))
        with uproot.open(path + filename) as f:
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

            TrigObj = ak.zip({
                "id": events["TrigObj_id"].array(),
                "filterBits": events["TrigObj_filterBits"].array(),
                "pt": events["TrigObj_pt"].array(),
                "eta": events["TrigObj_eta"].array(),
                "phi": events["TrigObj_phi"].array(),
                "nObj": events["nTrigObj"].array(),
            })

        OFFJets = ak.concatenate((OFFJets, OFFJet))
        HLTJets = ak.concatenate((HLTJets, HLTJet))
        MuonCollections = ak.concatenate((MuonCollections, MuonCollection))
        TrigObjs = ak.concatenate((TrigObjs, TrigObj))
    return OFFJets, HLTJets, MuonCollections, TrigObjs

def GetMaxMjj(Jets):
    jetcombo = ak.combinations(Jets,2, fields=["jet1","jet2"])
    jjsum  = jetcombo.jet1 + jetcombo.jet2
    maxmjj   = ak.max(jjsum.mass,axis=1)
    maxmjjindex = ak.Array(ak.to_list(np.expand_dims(ak.argmax(jjsum.mass,axis=1),axis=1)))
    maxmjjpair = jetcombo[maxmjjindex]
    return maxmjj, maxmjjpair, jjsum.mass # Retriving jets: maxmjjpair.jet1 ...

def GetMaxEta(Jets):
    JetCombo = ak.combinations(Jets,2, fields=["jet1","jet2"])
    etacombo = vector.Spatial.deltaeta(JetCombo.jet1, JetCombo.jet2)
    maxeta   = ak.max(abs(etacombo), axis=1)
    return maxeta, etacombo

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

def ApplyBasicCuts(OFFJets, HLTJets, MuonCollections, TrigObjs, analysis, triggerdict):
    print("number of events before BasicCuts: {}".format(len(OFFJets)))

    # This cut is made on jet level. So no events are lost. Don't have to cut HLTJets and MuonCollections.
    if (analysis!="LeadJetchEmEFAnalysis") and (analysis!="SubLeadJetchEmEFAnalysis"):
        chEmEFCut = (triggerdict["chEmEF"] > OFFJets.chEmEF)
        OFFJets = OFFJets[chEmEFCut]
        print("number of jets after chEmEFCut: {}".format(ak.sum(ak.num(OFFJets))))

    if (analysis!="LeadJetchHEFAnalysis") and (analysis!="SubLeadJetchHEFAnalysis"):
        chHEFCut = (triggerdict["chHEF"] < OFFJets.chHEF)
        OFFJets = OFFJets[chHEFCut]
        print("number of jets after chHEFCut: {}".format(ak.sum(ak.num(OFFJets))))

    if (analysis!="LeadJetneEmEFAnalysis") and (analysis!="SubLeadJetneEmEFAnalysis"):
        neEmEFCut = (triggerdict["neEmEF"] > OFFJets.neEmEF)
        OFFJets = OFFJets[neEmEFCut]
        print("number of jets after neEmEFCut: {}".format(ak.sum(ak.num(OFFJets))))

    if (analysis!="LeadJetneHEFAnalysis") and (analysis!="LeadJetneHEFAnalysis"):
        neHEFCut = (triggerdict["neHEF"] > OFFJets.neHEF)
        OFFJets = OFFJets[neHEFCut]
        print("number of jets after neHEFCut: {}".format(ak.sum(ak.num(OFFJets))))
    
    nJetCut = (ak.num(OFFJets)>=2)
    OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, nJetCut)
    TrigObjs = TrigObjs[nJetCut]
    print("number of events after nJetCut: {}".format(len(OFFJets)))

    # This cut is now passing an event if it has at least one (reasonably, i.e., muRelIso<0.2) isolated muon 
    MuonCuts = (ak.any((MuonCollections.Muon_pt>=27) & (MuonCollections.muRelIso<0.2), axis=1))
    OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, MuonCuts)
    TrigObjs = TrigObjs[MuonCuts]
    print("number of events after MuonCuts: {}".format(len(OFFJets)))

    IsoMu24Cut = HLTJets.IsoMu24
    OFFJets, HLTJets, MuonCollections = DoCuts(OFFJets, HLTJets, MuonCollections, IsoMu24Cut)
    TrigObjs = TrigObjs[IsoMu24Cut]
    print("number of events after IsoMu24Cut: {}".format(len(OFFJets)))

    print("BasicCuts Done!","\n")
    return OFFJets, HLTJets, MuonCollections, TrigObjs

def ApplyTriggerCuts(OFFJets, HLTJets, MuonCollections, TrigObjs, analysis, triggerdict):
    OFFcombo = ak.combinations(OFFJets,2, fields=["jet1","jet2"])
    print("number of jet pairs before cuts: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="LeadJetPtAnalysis":
        leadjetptcut = (OFFcombo.jet1.pt>=triggerdict["leadjetpt"])
        OFFcombo = OFFcombo[leadjetptcut]
        print("number of jet pairs after leadjetptcut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="SubleadJetPtAnalysis":
        subleadjetptcut = (OFFcombo.jet2.pt>=triggerdict["subleadjetpt"])
        OFFcombo = OFFcombo[subleadjetptcut]
        print("number of jet pairs after subleadjetptcut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="MjjAnalysis":
        jjsum  = OFFcombo.jet1 + OFFcombo.jet2
        mjjcut = (jjsum.mass>=triggerdict["mjj"])
        OFFcombo = OFFcombo[mjjcut]
        print("number of jet pairs after mjjcut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="DetaAnalysis":
        detas = vector.Spatial.deltaeta(OFFcombo.jet1, OFFcombo.jet2)
        detacut = (detas >= triggerdict["deta"])
        OFFcombo = OFFcombo[detacut]
        print("number of jet pairs after detacut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    eventcut = ak.where(ak.num(OFFcombo)>0,True, False)
    OFFcombo = OFFcombo[eventcut]
    OFFJets = OFFJets[eventcut]
    HLTJets = HLTJets[eventcut]
    MuonCollections = MuonCollections[eventcut] # Do we need this?
    TrigObjs = TrigObjs[eventcut]
    print("number of survived events: ", len(OFFJets))

    print("TriggerCuts Done!\n")
    return OFFJets, HLTJets, MuonCollections, TrigObjs, OFFcombo

def SelectHLTJetsCand(Jets, OFFcombo): # OFFcombo from ApplyTriggerCuts!!!
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
    shouldPassHLT_Jets = Jets[jetmask]

    # for events that have multiple jet pairs that pass HLT trigger path, I'm now selecting the jet pair that creates maxmjj.
    # 230726: this part is currently not used in the efficiency script
    j1, j2 = OFFcombo.jet1, OFFcombo.jet2
    jj = j1+j2
    argmaxmjj = ak.Array(ak.to_list(np.expand_dims(ak.argmax(jj.mass, axis=1),axis=1)))
    shouldPassHLT_MaxMjjCombo = OFFcombo[argmaxmjj]
    shouldPassHLT_mjjs = jj.mass
    shouldPassHLT_detas = vector.Spatial.deltaeta(j1, j2)

    print("Successfully selected the HLT VBF candidate jets!\n")
    return shouldPassHLT_Jets, shouldPassHLT_MaxMjjCombo, shouldPassHLT_mjjs, shouldPassHLT_detas # retrieving maxmjjcombo: maxmjjcombo.jet1 gives leadjet, maxmjjcombo.jet2 gives subleadjet

def GetEfficiency(binsize, maxbin, HLTPassedQuantity, HLTCandQuantity):
    bincenters = np.arange(binsize,maxbin,2*binsize)
    effs = np.zeros(len(bincenters))
    errmin,errmax = np.zeros(len(bincenters)), np.zeros(len(bincenters))

    for i in range(len(bincenters)):
        minlim = round(bincenters[i] - binsize,5)
        maxlim = round(bincenters[i] + binsize,5)

        numerator = ak.count_nonzero(ak.where((HLTPassedQuantity>=minlim) & (HLTPassedQuantity<=maxlim), 1, 0))
        denominator = ak.count_nonzero(ak.where((HLTCandQuantity   >=minlim) & (HLTCandQuantity   <=maxlim), 1, 0))
        errmin[i],errmax[i] = clopper_pearson_interval(numerator,denominator,0.05)
        if denominator!=0: effs[i] = numerator/denominator
    yerrmin, yerrmax = np.nan_to_num(errmin), np.nan_to_num(errmax)

    return effs, yerrmin, yerrmax, bincenters

def AssignFilterBitsToOFFJets(TrigObjs, OFFJets, HLTJets, triggerpath):
    # This function matches jets in TrigObj to OFFJets, and assigns the masking value to OFFJets.

    # selecting jets from TrigObjs
    PickJetsCut = ak.where(TrigObjs.id==1, True, False)
    TrigObjs = TrigObjs[PickJetsCut] # jetwise cut

    # selecting jets that pass HLT VBF filterBits.
    rightmostbit = (TrigObjs.filterBits) & (-1*TrigObjs.filterBits)
    PassHLTVBFfBCut = (rightmostbit==1)|(rightmostbit==2)
    TrigObjs = TrigObjs[PassHLTVBFfBCut]

    # discarding the events in TrigObjs with no passing jets
    ExistTrigObjsCut = ak.where(ak.num(TrigObjs)==0, False, True)
    TrigObjs = TrigObjs[ExistTrigObjsCut]
    OFFJets = OFFJets[ExistTrigObjsCut]
    HLTJets = HLTJets[ExistTrigObjsCut]

    # Making combos
    TrigOFFcombo = ak.cartesian({"tri": TrigObjs, "off": OFFJets[:,np.newaxis]})
    dR = np.sqrt((TrigOFFcombo.tri.eta-TrigOFFcombo.off.eta)**2 + (TrigOFFcombo.tri.phi-TrigOFFcombo.off.phi)**2)

    # calculating minimum deltaR
    mindR = ak.min(dR,axis=-1)
    dropTrigObj = ak.where(mindR>0.1,False,True)
    TrigObjs = TrigObjs[dropTrigObj]
    dR = dR[dropTrigObj]

    # discarding events with no matching jets
    NoTrigObjCut = ak.where(ak.num(TrigObjs)==0,False,True)
    TrigObjs = TrigObjs[NoTrigObjCut]
    OFFJets = OFFJets[NoTrigObjCut]
    dR = dR[NoTrigObjCut]
    print(f"Number of events with matching jets: {len(OFFJets)}")

    # matching TrigObjs <-> OFFJets
    mindRindex = ak.argmin(dR,axis=-1)
    filterBitsToAdd = np.full(np.shape(ak.pad_none(OFFJets.eta,ak.max(ak.num(OFFJets.eta)),axis=-1)),-999)
    shapePreservation = ak.where(OFFJets.eta,True,True)
    shapePreservation = ak.fill_none(ak.pad_none(shapePreservation,ak.max(ak.num(shapePreservation)),axis=-1),False,axis=-1)
    
    ti = time()
    for idx, sub in enumerate(mindRindex):
        for i,j in enumerate(sub):
            filterBitsToAdd[idx][j] = TrigObjs.filterBits[idx][i]
    tf = time()
    print("time elapsed in loop: {}".format(tf-ti))

    filterBitsToAdd = ak.Array(filterBitsToAdd)[shapePreservation]
    JetPassedHLT = ak.where(filterBitsToAdd>0, True, False)

    # assigning filterBits and masking values to OFFJets
    OFFJets = ak.with_field(OFFJets, filterBitsToAdd ,"filterBits")
    OFFJets = ak.with_field(OFFJets, JetPassedHLT ,"JetPassedHLT")

    # selecting jets that passed VBF HLT trigger
    HLTPassed_OFFJets = OFFJets[OFFJets.JetPassedHLT]

    # Discard events where the number of HLT VBF passed jet is less than two
    DijetCut = ak.where(ak.num(HLTPassed_OFFJets)<2, False, True)
    HLTPassed_OFFJets = HLTPassed_OFFJets[DijetCut]
    HLTJets = HLTJets[DijetCut]

    # last clean up -- eventwise VHF HLT trigger
    HLTPassed_OFFJets = HLTPassed_OFFJets[HLTJets.pt105|HLTJets.pt105triple]
    if   triggerpath=="pt105Analysis": HLTPassed_OFFJets = HLTPassed_OFFJets[HLTJets.pt105|HLTJets.pt105triple]
    elif triggerpath=="pt125Analysis": HLTPassed_OFFJets = HLTPassed_OFFJets[HLTJets.pt105|HLTJets.pt105triple]
    
    print("Successfully assigned the filterBits to offline jets!")
    return TrigObjs, OFFJets, HLTPassed_OFFJets

def GetVardict(HLTPassed_OFFJets, HLTCandJets, analysis, triggerdict, shouldPassHLT_mjjs, shouldPassHLT_detas):
    if analysis=="LeadJetPtAnalysis":
        vardict = {
            "plotname": "leadpt",
            "binsize"  : 5,
            "HLTPassedQuantity": HLTPassed_OFFJets.pt[:,0],
            "HLTCandQuantity": HLTCandJets.pt[:,0],
            "maxbin": 250,
            "xlabel": r"Offline $p_T^{leadjet}$ (GeV)",
            "threshold": triggerdict["leadjetpt"],
        }

    if analysis=="SubleadJetPtAnalysis":
        vardict = {
            "plotname": "subleadpt",
            "binsize"  : 2,
            "HLTPassedQuantity": HLTPassed_OFFJets.pt[:,1],
            "HLTCandQuantity": HLTCandJets.pt[:,1],
            "maxbin": 150,
            "xlabel": r"Offline $p_T^{subleadjet}$ (GeV)",
            "threshold": triggerdict["subleadjetpt"],
        }

    if analysis=="MjjAnalysis":
        # Should keep an eye on this. 
        # If there are more than two jets in one event, I should either: 
        #   devise a function that picks the mjjs that are created by jets that have passing filterBits, or
        #   recreate jet pairs, calculate mjjs, and filter out the pairs that do not pass triggercuts.
        print(f"Number of events that have more than two HLTPassed_OFFJets: {ak.count_nonzero(ak.where(ak.num(HLTPassed_OFFJets)>2,1,0))}")
        passed_mjj = GetMaxMjj(HLTPassed_OFFJets)[-1] # There are always two jets that passed... Coincidence? or did I impose smth? Good for now tho.
        cand_mjj = shouldPassHLT_mjjs
        vardict = {
            "plotname": "mjj",
            "binsize"  : 50,
            "HLTPassedQuantity": ak.flatten(passed_mjj),
            "HLTCandQuantity": ak.flatten(cand_mjj),
            "maxbin": 2500,
            "xlabel": r"Offline $M_{jj}$ (GeV)",
            "threshold": triggerdict["mjj"],
        }

    if analysis=="DetaAnalysis":
        vardict = {
            "plotname": "deta",
            "binsize"  : 0.1,
            "HLTPassedQuantity": ak.flatten(GetMaxEta(HLTPassed_OFFJets)[-1]),
            "HLTCandQuantity": ak.flatten(shouldPassHLT_detas),
            "maxbin": 6,
            "xlabel": r"Offline $\Delta\eta$",
            "threshold": triggerdict["deta"],
        }
        print("nEvents with more than one detas: ", ak.count_nonzero(ak.where(ak.num(GetMaxEta(HLTPassed_OFFJets)[-1])>1, 1, 0)))

    # JetID analysis requires jet-wise efficiency calculation...in progress
    # Need more attention from this point on!

    # leadjet
    if analysis=="LeadJetchEmEFAnalysis":
        vardict = {
            "plotname": "LeadJetchEmEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": HLTPassed_OFFJets.chEmEF[:,0],
            "HLTCandQuantity": HLTCandJets.chEmEF[:,0],
            "maxbin": 1.0,
            "xlabel": "Leadjet chEmEF",
            "threshold": -999,
        }

    if analysis=="LeadJetchHEFAnalysis":
        vardict = {
            "plotname": "LeadJetchHEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": HLTPassed_OFFJets.chHEF[:,0],
            "HLTCandQuantity": HLTCandJets.chHEF[:,0],
            "maxbin": 1.0, # Should make bin to exceed 1, because in eff calc, I am binning the events so that quantity < maxbin, which does not include 1, while there are events with EF==1.
            "xlabel": "Leadjet chHEF",
            "threshold": -999,
        }

    if analysis=="LeadJetneEmEFAnalysis":
        vardict = {
            "plotname": "LeadJetneEmEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": HLTPassed_OFFJets.neEmEF[:,0],
            "HLTCandQuantity": HLTCandJets.neEmEF[:,0],
            "maxbin": 1.0,
            "xlabel": "Leadjet neEmEF",
            "threshold": -999,
        }

    if analysis=="LeadJetneHEFAnalysis":
        vardict = {
            "plotname": "LeadJetneHEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": HLTPassed_OFFJets.neHEF[:,0],
            "HLTCandQuantity": HLTCandJets.neHEF[:,0],
            "maxbin": 1.0,
            "xlabel": "Leadjet neHEF",
            "threshold": -999,
        }

    if analysis=="LeadJetmuEFAnalysis":
        vardict = {
            "plotname": "LeadJetmuEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": HLTPassed_OFFJets.muEF[:,0],
            "HLTCandQuantity": HLTCandJets.muEF[:,0],
            "maxbin": 1.0,
            "xlabel": "Leadjet muEF",
            "threshold": -999,
        }

    #subleadjet 
    if analysis=="SubLeadJetchEmEFAnalysis":
        vardict = {
            "plotname": "SubLeadJetchEmEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": HLTPassed_OFFJets.chEmEF[:,1],
            "HLTCandQuantity": HLTCandJets.chEmEF[:,1],
            "maxbin": 1.0,
            "xlabel": "SubLeadJet chEmEF",
            "threshold": -999,
        }

    if analysis=="SubLeadJetchHEFAnalysis":
        vardict = {
            "plotname": "SubLeadJetchHEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": HLTPassed_OFFJets.chHEF[:,1],
            "HLTCandQuantity": HLTCandJets.chHEF[:,1],
            "maxbin": 1.0, # Should make bin to exceed 1, because in eff calc, I am binning the events so that quantity < maxbin, which does not include 1, while there are events with EF==1.
            "xlabel": "SubLeadJet chHEF",
            "threshold": -999,
        }

    if analysis=="SubLeadJetneEmEFAnalysis":
        vardict = {
            "plotname": "SubLeadJetneEmEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": HLTPassed_OFFJets.neEmEF[:,1],
            "HLTCandQuantity": HLTCandJets.neEmEF[:,1],
            "maxbin": 1.0,
            "xlabel": "SubLeadJet neEmEF",
            "threshold": -999,
        }

    if analysis=="SubLeadJetneHEFAnalysis":
        vardict = {
            "plotname": "SubLeadJetneHEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": HLTPassed_OFFJets.neHEF[:,1],
            "HLTCandQuantity": HLTCandJets.neHEF[:,1],
            "maxbin": 1.0,
            "xlabel": "SubLeadJet neHEF",
            "threshold": -999,
        }

    if analysis=="SubLeadJetmuEFAnalysis":
        vardict = {
            "plotname": "SubLeadJetmuEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": HLTPassed_OFFJets.muEF[:,1],
            "HLTCandQuantity": HLTCandJets.muEF[:,1],
            "maxbin": 1.0,
            "xlabel": "SubLeadJet muEF",
            "threshold": -999,
        }
    return vardict
