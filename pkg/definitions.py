"""
    This script contains the function definitions used in HLT VBF Trigger efficiency analysis for Run3 Summer2023 data.
    Raymond Kil, 2023
"""

import numpy as np
import awkward as ak
import uproot
import vector
from scipy.stats import beta
import json

def MakeObjects(filenames,path):
    OFFJets, HLTJets, MuonCollections, TrigObjs, Luminosities = [],ak.Array([]), [], [], []
    for filename in filenames:
        print("Processing file {0}".format(filename))
        with uproot.open(path + filename) as f:
            events = f["Events"]

            HLTJet = ak.zip({
                "pt105"      : events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5"].array(),
                "pt105triple": events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5_TriplePFJet"].array(),
                "pt125"      : events["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0"].array(),
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
                "muRelIso": events["Muon_pfRelIso04_all"].array()
            })

            TrigObj = ak.zip({
                "id": events["TrigObj_id"].array(),
                "filterBits": events["TrigObj_filterBits"].array(),
                "pt": events["TrigObj_pt"].array(),
                "eta": events["TrigObj_eta"].array(),
                "phi": events["TrigObj_phi"].array(),
                "nObj": events["nTrigObj"].array(),
            })

            Luminosity = ak.zip({
                "lum": events["luminosityBlock"].array(),
                "run": events["run"].array()
            })

        OFFJets = ak.concatenate((OFFJets, OFFJet))
        HLTJets = ak.concatenate((HLTJets, HLTJet))
        MuonCollections = ak.concatenate((MuonCollections, MuonCollection))
        TrigObjs = ak.concatenate((TrigObjs, TrigObj))
        Luminosities = ak.concatenate((Luminosities, Luminosity))
    return OFFJets, HLTJets, MuonCollections, TrigObjs, Luminosities

def GetTriggerDict(triggerpath, analysis, TightCuts):
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
    return triggerdict

def LoadDataset(whichfiles, datapath, useC, useD, combined, subset=""):
    if whichfiles=="singlemuon":
        if useC:
            datasetC = {
                "OFFJets": MakeVector(ak.from_parquet(f"{datapath}*C_OFFJets{subset}*.parquet")),
                "HLTJets": ak.from_parquet(f"{datapath}*C_HLTJets{subset}*.parquet"),
                "MuonCollections": ak.from_parquet(f"{datapath}*C_MuonCollections{subset}*.parquet"),
                "TrigObjs": ak.from_parquet(f"{datapath}*C_TrigObjs{subset}*.parquet"),
                "Luminosities": ak.from_parquet(f"{datapath}*C_Luminosities{subset}*.parquet"),
                "color": "tab:blue",
                "label": "C"
            }

        if useD:
            datasetD = {
                "OFFJets": MakeVector(ak.from_parquet(f"{datapath}*D_OFFJets{subset}*.parquet")),
                "HLTJets": ak.from_parquet(f"{datapath}*D_HLTJets{subset}*.parquet"),
                "MuonCollections": ak.from_parquet(f"{datapath}*D_MuonCollections{subset}*.parquet"),
                "TrigObjs": ak.from_parquet(f"{datapath}*D_TrigObjs{subset}*.parquet"),
                "Luminosities": ak.from_parquet(f"{datapath}*D_Luminosities{subset}*.parquet"),
                "color": "tab:red",
                "label": "D"
            }

        if useC and useD and combined:
            dataset = {
                "OFFJets": ak.concatenate((datasetC["OFFJets"],datasetD["OFFJets"])),
                "HLTJets": ak.concatenate((datasetC["HLTJets"],datasetD["HLTJets"])),
                "MuonCollections": ak.concatenate((datasetC["MuonCollections"],datasetD["MuonCollections"])),
                "TrigObjs": ak.concatenate((datasetC["TrigObjs"],datasetD["TrigObjs"])),
                "Luminosities": ak.concatenate((datasetC["Luminosities"],datasetD["Luminosities"])),
                "color": "tab:blue",
                "label": ""
            }

        if   not useD: 
            datasets = [datasetC]
            print(f"Object loading done! nEvents: {len(datasets[0]['OFFJets'])}")
        elif not useC: 
            datasets = [datasetD]
            print(f"Object loading done! nEvents: {len(datasets[0]['OFFJets'])}")
        elif not combined: 
            datasets = [datasetC, datasetD]
            print(f"Object loading done! nEvents in C: {len(datasets[0]['OFFJets'])} nEvents in D: {len(datasets[1]['OFFJets'])}")
        elif combined:
            datasets = [dataset]
            print(f"Object loading done! nEvents: {len(datasets[0]['OFFJets'])}")
    # if whichfiles=="zerobias":
    return datasets

def GetClopperPearsonInterval(hltPassed, total, alpha):
    min, max = beta.ppf(alpha, hltPassed, total - hltPassed + 1), beta.ppf(1 - alpha, hltPassed + 1, total - hltPassed)
    center = 0
    if total !=0: center = hltPassed/total
    min, max = center-min , max-center
    return min, max

def DoCuts(cut, OFFJets="", HLTJets="", MuonCollections="", TrigObjs="", METCollections="", JetCombo=""):
    # Should manually choose which ones to return when the function is called.
    if len(OFFJets)        : OFFJets = OFFJets[cut]
    if len(HLTJets)        : HLTJets = HLTJets[cut]
    if len(MuonCollections): MuonCollections = MuonCollections[cut]
    if len(TrigObjs)       : TrigObjs = TrigObjs[cut]
    if len(METCollections) : METCollections = METCollections[cut]
    if len(JetCombo)       : JetCombo = JetCombo[cut]
    return OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections, JetCombo

def MakeGolden(OFFJets, HLTJets, MuonCollections, TrigObjs, Luminosities, goldenpath):
    """
        This function cuts the events that are not in golden luminosity blocks, and returns the cut objects.
    """
    goldenJSON = json.load(open(goldenpath))

    # expanding goldenJSON
    expanded_golden = {}
    for run in goldenJSON.keys():
        block = np.array([], dtype=int)
        for b in goldenJSON[run]:
            block = np.append(block, np.arange(b[0], b[1]+1))
        expanded_golden.update({run:list(block)})
    
    # creating dict that groups the lumi of events by runs
    event_runs = {}
    run, lum = Luminosities.run, Luminosities.lum
    print("run len", len(run))
    for r,l in zip(run, lum):
        r = str(r)
        if r not in event_runs: event_runs[r] = [l]
        elif r in event_runs: event_runs[r].append(l)
        else: pass

    # for each run, checking if events lumis are in golden
    goldencut = []
    for event_run in event_runs.keys():
        event_run = str(event_run)
        if event_run in expanded_golden.keys():
            goldencut.append(np.isin(event_runs[event_run],expanded_golden[event_run]))
        else:
            goldencut.append(np.full_like(event_runs[event_run], False, dtype=bool))
    goldencut = ak.Array(np.concatenate(goldencut))
    print("len goldencut",len(goldencut))

    # cut the events
    print(f"Number of events before goldencuts: {len(OFFJets)}")
    OFFJets, HLTJets, MuonCollections, TrigObjs = DoCuts(goldencut, OFFJets=OFFJets, HLTJets=HLTJets, MuonCollections=MuonCollections, TrigObjs=TrigObjs)[:4]
    print(f"Number of events after goldencuts: {len(OFFJets)}\n")
    return OFFJets, HLTJets, MuonCollections, TrigObjs

def MakeVector(OFFJets):
    """
        This function converts an ak zipped object to vector zipped object. 
        OFFJets needs this when loaded from parquet.
    """
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
    return OFFJets

def ApplyBasicCuts(OFFJets, HLTJets, MuonCollections, TrigObjs, analysis, triggerdict):
    print("number of events before BasicCuts: {}".format(len(OFFJets)))

    # This cut is made on jet level. So no events are lost. Don't have to cut HLTJets and MuonCollections.
    if (analysis!="LeadJetchEmEFAnalysis") and (analysis!="SubLeadJetchEmEFAnalysis"):
        chEmEFCut = (triggerdict["chEmEF"] > OFFJets.chEmEF)
        OFFJets = DoCuts(chEmEFCut, OFFJets=OFFJets)[0]
        print(f"number of jets after chEmEFCut: {format(ak.sum(ak.num(OFFJets)))}")

    if (analysis!="LeadJetchHEFAnalysis") and (analysis!="SubLeadJetchHEFAnalysis"):
        chHEFCut = (triggerdict["chHEF"] < OFFJets.chHEF)
        OFFJets = DoCuts(chHEFCut, OFFJets=OFFJets)[0]
        print(f"number of jets after chHEFCut: {format(ak.sum(ak.num(OFFJets)))}")

    if (analysis!="LeadJetneEmEFAnalysis") and (analysis!="SubLeadJetneEmEFAnalysis"):
        neEmEFCut = (triggerdict["neEmEF"] > OFFJets.neEmEF)
        OFFJets = DoCuts(neEmEFCut, OFFJets=OFFJets)[0]
        print(f"number of jets after neEmEFCut: {format(ak.sum(ak.num(OFFJets)))}")

    if (analysis!="LeadJetneHEFAnalysis") and (analysis!="LeadJetneHEFAnalysis"):
        neHEFCut = (triggerdict["neHEF"] > OFFJets.neHEF)
        OFFJets = DoCuts(neHEFCut, OFFJets=OFFJets)[0]
        print(f"number of jets after neHEFCut: {format(ak.sum(ak.num(OFFJets)))}")

    nJetCut = (ak.num(OFFJets)>=2)
    OFFJets, HLTJets, MuonCollections, TrigObjs = DoCuts(nJetCut, OFFJets=OFFJets, HLTJets=HLTJets, MuonCollections=MuonCollections, TrigObjs=TrigObjs)[:4]
    print(f"number of events after nJetCut: {format(len(OFFJets))}")

    # This cut is now passing an event if it has at least one (reasonably, i.e., muRelIso<0.2) isolated muon 
    MuonCuts = (ak.any((MuonCollections.Muon_pt>=27) & (MuonCollections.muRelIso<0.2), axis=1))
    OFFJets, HLTJets, MuonCollections, TrigObjs = DoCuts(MuonCuts, OFFJets=OFFJets, HLTJets=HLTJets, MuonCollections=MuonCollections, TrigObjs=TrigObjs)[:4]
    print(f"number of events after MuonCuts: {format(len(OFFJets))}")

    IsoMu24Cut = HLTJets.IsoMu24
    OFFJets, HLTJets, MuonCollections, TrigObjs = DoCuts(IsoMu24Cut, OFFJets=OFFJets, HLTJets=HLTJets, MuonCollections=MuonCollections, TrigObjs=TrigObjs)[:4]
    print(f"number of events after IsoMu24Cut: {format(len(OFFJets))}")

    print("BasicCuts Done!","\n")
    return OFFJets, HLTJets, MuonCollections, TrigObjs

def ApplyTriggerCuts(OFFJets, HLTJets, TrigObjs, analysis, triggerdict):
    OFFcombo = ak.combinations(OFFJets,2, fields=["jet1","jet2"])
    print("number of jet pairs before cuts: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="LeadJetPtAnalysis":
        leadjetptcut = (OFFcombo.jet1.pt>=triggerdict["leadjetpt"])
        OFFcombo = DoCuts(leadjetptcut, JetCombo=OFFcombo)[-1]
        print("number of jet pairs after leadjetptcut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="SubleadJetPtAnalysis":
        subleadjetptcut = (OFFcombo.jet2.pt>=triggerdict["subleadjetpt"])
        OFFcombo = DoCuts(subleadjetptcut, JetCombo=OFFcombo)[-1]
        print("number of jet pairs after subleadjetptcut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="MjjAnalysis":
        jjsum  = OFFcombo.jet1 + OFFcombo.jet2
        mjjcut = (jjsum.mass>=triggerdict["mjj"])
        OFFcombo = DoCuts(mjjcut, JetCombo=OFFcombo)[-1]
        print("number of jet pairs after mjjcut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="DetaAnalysis":
        detas = vector.Spatial.deltaeta(OFFcombo.jet1, OFFcombo.jet2)
        detacut = (detas >= triggerdict["deta"])
        OFFcombo = DoCuts(detacut, JetCombo=OFFcombo)[-1]
        print("number of jet pairs after detacut: ", ak.count_nonzero(OFFcombo.jet1.pt))

    eventcut = ak.where(ak.num(OFFcombo)>0,True, False) # cutting events where no jet pair is left after cuts
    OFFJets, HLTJets, mu_placeholder, TrigObjs, met_placeholder, OFFcombo = DoCuts(eventcut, OFFJets=OFFJets, HLTJets=HLTJets, TrigObjs=TrigObjs, JetCombo=OFFcombo)
    print("number of survived events: ", len(OFFJets))
    print("TriggerCuts Done!\n")
    return OFFJets, HLTJets, TrigObjs, OFFcombo

def AssignFilterBitsToOFFJets(OFFJets, HLTJets, TrigObjs):
    """
        This function makes cuts on TrigObjs, matches jets in TrigObj to OFFJets, and assigns the filterBits to OFFJets.
    """
    
    # selecting jets from TrigObjs
    PickJetsCut = ak.where(TrigObjs.id==1, True, False)
    TrigObjs = DoCuts(PickJetsCut, TrigObjs=TrigObjs)[3] # jetwise cut

    # selecting TrigObjs jets that pass HLT VBF filterBits.
    """
    rightmostbit = (TrigObjs.filterBits) & (-1*TrigObjs.filterBits)
    PassHLTVBFfBCut = (rightmostbit==1)|(rightmostbit==2)
    TrigObjs = DoCuts(PassHLTVBFfBCut, TrigObjs=TrigObjs)[3]
    """

    # discarding the events in TrigObjs with no passing jets
    ExistTrigObjsCut = ak.where(ak.num(TrigObjs)==0, False, True)
    OFFJets, HLTJets, mu_placeholder, TrigObjs = DoCuts(ExistTrigObjsCut, OFFJets=OFFJets, HLTJets=HLTJets, TrigObjs=TrigObjs)[:4]

    # Making trig-off combos
    TrigOFFcombo = ak.cartesian({"tri": TrigObjs, "off": OFFJets[:,np.newaxis]})
    dR = np.sqrt((TrigOFFcombo.tri.eta-TrigOFFcombo.off.eta)**2 + (TrigOFFcombo.tri.phi-TrigOFFcombo.off.phi)**2)

    # calculating minimum deltaR
    mindR = ak.min(dR,axis=-1)
    dropTrigObj = ak.where(mindR>0.1,False,True)
    TrigObjs = DoCuts(dropTrigObj, TrigObjs=TrigObjs)[3]
    dR = dR[dropTrigObj]

    # discarding events with no matching jets
    NoTrigObjCut = ak.where(ak.num(TrigObjs)==0,False,True)
    OFFJets, HLTJets, mu_placeholder, TrigObjs = DoCuts(NoTrigObjCut, OFFJets=OFFJets, HLTJets=HLTJets, TrigObjs=TrigObjs)[:4]
    dR = dR[NoTrigObjCut]
    print(f"Number of events with matching jets: {len(OFFJets)}")

    # matching TrigObjs <-> OFFJets
    mindRindex = ak.argmin(dR,axis=-1)
    filterBitsToAdd = np.full(np.shape(ak.pad_none(OFFJets.eta,ak.max(ak.num(OFFJets.eta))+1,axis=-1)),-999)
    event_index = np.expand_dims(np.arange(len(filterBitsToAdd)),-1)
    mindRindex = ak.fill_none(ak.pad_none(mindRindex,ak.max(ak.num(mindRindex))),-1)
    filterBits = ak.fill_none(ak.pad_none(TrigObjs.filterBits,ak.max(ak.num(TrigObjs.filterBits))),-999)
    filterBitsToAdd[event_index,mindRindex] = filterBits
    shape_preservation = ak.full_like(OFFJets.eta, True, dtype=bool)
    shape_preservation = ak.fill_none(ak.pad_none(shape_preservation,ak.max(ak.num(OFFJets))+1),False)
    filterBitsToAdd = ak.Array(filterBitsToAdd)[shape_preservation]
    JetPassedHLT = ak.where(filterBitsToAdd>0, True, False) # jet-level boolean if jets passed HLT or not

    # assigning filterBits and masking values to OFFJets
    OFFJets = ak.with_field(OFFJets, filterBitsToAdd ,"filterBits")
    OFFJets = ak.with_field(OFFJets, JetPassedHLT ,"JetPassedHLT")
    print("len after assigning filterBits",len(OFFJets))

    print("Successfully assigned the filterBits to offline jets!\n")
    return OFFJets, HLTJets, TrigObjs

def SelectHLTJetsCand(OFFJets, OFFcombo):
    """
        This function selects the jets that should pass the HLT from OFFJets.
        It is selecting the jets in OFFJets that are also in OFFcombo, 
        as OFFcombo only contains the jets that survive the trigger cuts and thus should pass HLT.
    """

    # Reshaping Jets 
    exp_OFFcombo_jet1, exp_OFFJets_pt = ak.broadcast_arrays(OFFcombo.jet1, OFFJets.pt[:,np.newaxis], depth_limit=2) 
    exp_OFFcombo_jet2, exp_OFFJets_pt = ak.broadcast_arrays(OFFcombo.jet2, OFFJets.pt[:,np.newaxis], depth_limit=2)

    # Picking OFFcombo jets in Jets
    jet1mask = ak.where(exp_OFFJets_pt==exp_OFFcombo_jet1.pt,True,False) # leadjet
    jet2mask = ak.where(exp_OFFJets_pt==exp_OFFcombo_jet2.pt,True,False) # subleadjet

    # Rectangularizing masks
    padding_target = ak.max(ak.num(OFFJets.pt))
    padded_jet1mask, padded_jet2mask = ak.pad_none(jet1mask, padding_target, axis=1), ak.pad_none(jet2mask, padding_target, axis=1)
    padded_jet1mask, padded_jet2mask = ak.fill_none(padded_jet1mask,[False],axis=1), ak.fill_none(padded_jet2mask,[False],axis=1)
    padded_jet1mask, padded_jet2mask = ak.pad_none(padded_jet1mask,ak.max(ak.num(padded_jet1mask,axis=2)),axis=2), ak.pad_none(padded_jet2mask,ak.max(ak.num(padded_jet2mask,axis=2)),axis=2)

    # Swapping axes
    padded_jet1mask, padded_jet2mask = ak.to_numpy(padded_jet1mask,allow_missing=True), ak.to_numpy(padded_jet2mask,allow_missing=True)
    swapped_jet1mask, swapped_jet2mask = np.swapaxes(padded_jet1mask,0,1), np.swapaxes(padded_jet2mask,0,1)
    swapped_jet1mask, swapped_jet2mask = ak.any(swapped_jet1mask,axis=0), ak.any(swapped_jet2mask,axis=0)

    # selecting jets that should pass HLT
    jetmask = (swapped_jet1mask)|(swapped_jet2mask)
    cutbool = ak.fill_none(ak.pad_none(ak.where(OFFJets.pt!=-999, True, False), padding_target, axis=-1), False)
    jetmask = jetmask[cutbool]
    shouldPassHLT_Jets  = OFFJets[jetmask]
    shouldPassHLT_combo = OFFcombo # The input OFFcombo is already the jet combos that should pass the HLT.

    print("Successfully selected the HLT VBF candidate jets!\n")
    return shouldPassHLT_Jets, shouldPassHLT_combo

def GetNumDenom(shouldPassHLT_Jets, HLTJets, OFFcombo, analysis, triggerpath, filterbits=True):
    """
        This function gets the numerator and denominator that are fed into efficiency calculation.
        The numerator and denominator are defined in a different way for single-jet quantities (pT and EF) and double-jet quantities (mjj and deta).
        So the function is divided into two-parts: single-jet quantity and double-jet quantity.
    """

    # single-jet quantity (pTs and EFs)
    if "Pt" in analysis or "EF" in analysis:
        ### DENOMINATOR ###
        shouldPassHLT_Jets = shouldPassHLT_Jets

        ### NUMERATOR ###
        # event-level trigger path cut
        print(f"Number of events BEFORE trigger path cut: {len(shouldPassHLT_Jets)}")
        if   triggerpath=="pt105Analysis": trigpassed_OFFJets = shouldPassHLT_Jets[HLTJets.pt105|HLTJets.pt105triple]
        elif triggerpath=="pt125Analysis": trigpassed_OFFJets = shouldPassHLT_Jets[HLTJets.pt125|HLTJets.pt125triple]
        print(f"Number of events AFTER  trigger path cut: {len(trigpassed_OFFJets)}")

        if filterbits:
            # selecting jets that passed VBF HLT trigger
            print(f"Number of jets BEFORE filerBits cut: {ak.count(trigpassed_OFFJets)}")
            fbpassed_OFFJets = trigpassed_OFFJets[trigpassed_OFFJets.JetPassedHLT]
            print(f"Number of jets AFTER  filerBits cut: {ak.count(fbpassed_OFFJets)}")

            # Discard events where the number of HLT VBF passed jet is less than one
            print(f"Number of events BEFORE onejetcut cut: {len(fbpassed_OFFJets)}")
            onejetcut = ak.where(ak.num(fbpassed_OFFJets)>=1, True, False)
            passed_OFFJets, HLTJets = DoCuts(onejetcut, OFFJets=fbpassed_OFFJets, HLTJets=HLTJets)[:2]
            print(f"Number of events AFTER  onejetcut cut: {len(passed_OFFJets)}")

            print("GetNumDenom done! fbpassed_OFFJets are returned.")
        else:
            passed_OFFJets = trigpassed_OFFJets
            print("GetNumDenom done! trigpassed_OFFJets are returned.")

        return shouldPassHLT_Jets, passed_OFFJets

    # double-jet quantity (mjj and deta)
    elif "Mjj" in analysis or "Deta" in analysis:
        ### DENOMINATOR ###
        shouldPass_jjsum = OFFcombo.jet1 + OFFcombo.jet2
        shouldPass_mjj = shouldPass_jjsum.mass
        shouldPass_deta = vector.Spatial.deltaeta(OFFcombo.jet1, OFFcombo.jet2)

        ### NUMERATOR ###
        # event-level trigger path cut
        print(f"Number of events BEFORE trigger path cut: {len(OFFcombo)}")
        if   triggerpath=="pt105Analysis": trigpassed_OFFcombo = OFFcombo[HLTJets.pt105|HLTJets.pt105triple]
        elif triggerpath=="pt125Analysis": trigpassed_OFFcombo = OFFcombo[HLTJets.pt125|HLTJets.pt125triple]
        print(f"Number of events AFTER  trigger path cut: {len(trigpassed_OFFcombo)}")

        if filterbits:
            # jet-level filterBits cut
            fbcut = trigpassed_OFFcombo.jet1.JetPassedHLT & trigpassed_OFFcombo.jet2.JetPassedHLT
            fbpassed_combo_j1, fbpassed_combo_j2 = trigpassed_OFFcombo.jet1[fbcut], trigpassed_OFFcombo.jet2[fbcut]

            passed_jjsum = fbpassed_combo_j1 + fbpassed_combo_j2
            passed_mjj   = passed_jjsum.mass
            passed_deta  = vector.Spatial.deltaeta(fbpassed_combo_j1, fbpassed_combo_j2)
        else:
            passed_jjsum = trigpassed_OFFcombo.jet1 + trigpassed_OFFcombo.jet2
            passed_mjj   = passed_jjsum.mass
            passed_deta  = vector.Spatial.deltaeta(trigpassed_OFFcombo.jet1, trigpassed_OFFcombo.jet1)

        if analysis=="MjjAnalysis" : 
            print(f"GetNumDenom done! mjjs are returned. filterBits: {filterbits}")
            return ak.flatten(shouldPass_mjj) , ak.flatten(passed_mjj)
        if analysis=="DetaAnalysis": 
            print(f"GetNumDenom done! detas are returned. filterBits: {filterbits}")
            return ak.flatten(shouldPass_deta), ak.flatten(passed_deta)
    
    else: print("what is your problem? Give me a sensible analysis quantity.")

def GetEfficiency(binsize, maxbin, HLTPassedQuantity, HLTCandQuantity):
    bincenters = np.arange(binsize,maxbin,2*binsize)
    effs = np.zeros(len(bincenters))
    errmin,errmax = np.zeros(len(bincenters)), np.zeros(len(bincenters))

    for i in range(len(bincenters)):
        minlim = round(bincenters[i] - binsize,5)
        maxlim = round(bincenters[i] + binsize,5)

        numerator = ak.count_nonzero(ak.where((HLTPassedQuantity>=minlim) & (HLTPassedQuantity<=maxlim), 1, 0))
        denominator = ak.count_nonzero(ak.where((HLTCandQuantity   >=minlim) & (HLTCandQuantity   <=maxlim), 1, 0))
        errmin[i],errmax[i] = GetClopperPearsonInterval(numerator,denominator,0.05)
        if denominator!=0: effs[i] = numerator/denominator
    yerrmin, yerrmax = np.nan_to_num(errmin), np.nan_to_num(errmax)

    return effs, yerrmin, yerrmax, bincenters

def GetVardict(passedQuantity, shouldPassQuantity, analysis, triggerdict):
    if analysis=="LeadJetPtAnalysis":
        vardict = {
            "plotname": "leadpt",
            "binsize"  : 5,
            "HLTPassedQuantity": passedQuantity.pt[:,0],
            "HLTCandQuantity": shouldPassQuantity.pt[:,0],
            "maxbin": 250,
            "xlabel": r"$p_T^{leadjet}$ (GeV)",
            "threshold": triggerdict["leadjetpt"],
        }

    if analysis=="SubleadJetPtAnalysis":
        vardict = {
            "plotname": "subleadpt",
            "binsize"  : 2,
            "HLTPassedQuantity": passedQuantity.pt[:,1],
            "HLTCandQuantity": shouldPassQuantity.pt[:,1],
            "maxbin": 150,
            "xlabel": r"$p_T^{subleadjet}$ (GeV)",
            "threshold": triggerdict["subleadjetpt"],
        }

    if analysis=="MjjAnalysis":
        vardict = {
            "plotname": "mjj",
            "binsize"  : 50,
            "HLTPassedQuantity": passedQuantity,
            "HLTCandQuantity": shouldPassQuantity,
            "maxbin": 2500,
            "xlabel": r"$M_{jj}$ (GeV)",
            "threshold": triggerdict["mjj"],
        }

    if analysis=="DetaAnalysis":
        vardict = {
            "plotname": "deta",
            "binsize"  : 0.1,
            "HLTPassedQuantity": passedQuantity,
            "HLTCandQuantity": shouldPassQuantity,
            "maxbin": 6,
            "xlabel": r"$\Delta\eta$",
            "threshold": triggerdict["deta"],
        }

    if analysis=="LeadJetchEmEFAnalysis":
        vardict = {
            "plotname": "LeadJetchEmEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": passedQuantity.chEmEF[:,0],
            "HLTCandQuantity": shouldPassQuantity.chEmEF[:,0],
            "maxbin": 1.0,
            "xlabel": "Leadjet chEmEF",
            "threshold": -999,
        }

    if analysis=="LeadJetchHEFAnalysis":
        vardict = {
            "plotname": "LeadJetchHEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": passedQuantity.chHEF[:,0],
            "HLTCandQuantity": shouldPassQuantity.chHEF[:,0],
            "maxbin": 1.0, # Should make bin to exceed 1, because in eff calc, I am binning the events so that quantity < maxbin, which does not include 1, while there are events with EF==1.
            "xlabel": "Leadjet chHEF",
            "threshold": -999,
        }

    if analysis=="LeadJetneEmEFAnalysis":
        vardict = {
            "plotname": "LeadJetneEmEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": passedQuantity.neEmEF[:,0],
            "HLTCandQuantity": shouldPassQuantity.neEmEF[:,0],
            "maxbin": 1.0,
            "xlabel": "Leadjet neEmEF",
            "threshold": -999,
        }

    if analysis=="LeadJetneHEFAnalysis":
        vardict = {
            "plotname": "LeadJetneHEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": passedQuantity.neHEF[:,0],
            "HLTCandQuantity": shouldPassQuantity.neHEF[:,0],
            "maxbin": 1.0,
            "xlabel": "Leadjet neHEF",
            "threshold": -999,
        }

    if analysis=="LeadJetmuEFAnalysis":
        vardict = {
            "plotname": "LeadJetmuEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": passedQuantity.muEF[:,0],
            "HLTCandQuantity": shouldPassQuantity.muEF[:,0],
            "maxbin": 1.0,
            "xlabel": "Leadjet muEF",
            "threshold": -999,
        }

    if analysis=="SubLeadJetchEmEFAnalysis":
        vardict = {
            "plotname": "SubLeadJetchEmEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": passedQuantity.chEmEF[:,1],
            "HLTCandQuantity": shouldPassQuantity.chEmEF[:,1],
            "maxbin": 1.0,
            "xlabel": "SubLeadJet chEmEF",
            "threshold": -999,
        }

    if analysis=="SubLeadJetchHEFAnalysis":
        vardict = {
            "plotname": "SubLeadJetchHEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": passedQuantity.chHEF[:,1],
            "HLTCandQuantity": shouldPassQuantity.chHEF[:,1],
            "maxbin": 1.0,
            "xlabel": "SubLeadJet chHEF",
            "threshold": -999,
        }

    if analysis=="SubLeadJetneEmEFAnalysis":
        vardict = {
            "plotname": "SubLeadJetneEmEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": passedQuantity.neEmEF[:,1],
            "HLTCandQuantity": shouldPassQuantity.neEmEF[:,1],
            "maxbin": 1.0,
            "xlabel": "SubLeadJet neEmEF",
            "threshold": -999,
        }

    if analysis=="SubLeadJetneHEFAnalysis":
        vardict = {
            "plotname": "SubLeadJetneHEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": passedQuantity.neHEF[:,1],
            "HLTCandQuantity": shouldPassQuantity.neHEF[:,1],
            "maxbin": 1.0,
            "xlabel": "SubLeadJet neHEF",
            "threshold": -999,
        }

    if analysis=="SubLeadJetmuEFAnalysis":
        vardict = {
            "plotname": "SubLeadJetmuEF",
            "binsize"  : 0.025,
            "HLTPassedQuantity": passedQuantity.muEF[:,1],
            "HLTCandQuantity": shouldPassQuantity.muEF[:,1],
            "maxbin": 1.0,
            "xlabel": "SubLeadJet muEF",
            "threshold": -999,
        }
    return vardict