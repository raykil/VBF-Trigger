"""
    This script contains the function definitions used in HLT VBF Trigger efficiency analysis for Run3 data.
    Raymond Kil, 2023
"""
import numpy as np
import awkward as ak
import uproot
import vector
from scipy.stats import beta
import json
import os 

### ANALYSIS ###

def MakeHLT(filenames, path):
    HLTJets = ak.Array([])
    for filename in filenames:
        print(f"Processing file {filename}")
        try: 
            with uproot.open(path + filename) as f:
                events = f["Events"]

                HLTJet = ak.zip({
                    "IsoMu24": events["HLT_IsoMu24"].array(),
                    "IsoMu27": events["HLT_IsoMu27"].array()
                })
                if "HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5" in events.keys() and "HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5_TriplePFJet" in events.keys():
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5"].array()            , where="pt105")
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5_TriplePFJet"].array(), where="pt105triple")

                if "HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0"  in events.keys() and "HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0_TriplePFJet"  in events.keys():
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0"].array()            , where="pt125")
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0_TriplePFJet"].array(), where="pt125triple")

                if "HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85" in events.keys() and "HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85_TriplePFJet" in events.keys():
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85"].array()            , where="pt75")
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85_TriplePFJet"].array(), where="pt75triple")
                
                if "HLT_VBF_DiPFJet80_45_Mjj500_Detajj2p5_PFMET85" in events.keys() and "HLT_VBF_DiPFJet80_45_Mjj500_Detajj2p5_PFMET85_TriplePFJet" in events.keys():
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet80_45_Mjj500_Detajj2p5_PFMET85"].array()            , where="pt80")
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet80_45_Mjj500_Detajj2p5_PFMET85_TriplePFJet"].array(), where="pt80triple")
                
                if "HLT_DiJet110_35_Mjj650_PFMET110" in events.keys():
                    HLTJet = ak.with_field(HLTJet, events["HLT_DiJet110_35_Mjj650_PFMET110"].array(), where="pt110")

            HLTJets = ak.concatenate((HLTJets, HLTJet))
        except (OSError, uproot.exceptions.KeyInFileError) as e: print(f"{path+filename} failed because of {e}. Skipping for now...")
    return HLTJets

def MakeObjects(rootfiles):
    OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections, Luminosities = [],ak.Array([]), [], [], [], []
    for filename in rootfiles:
        print(f"Processing file {filename}...")
        try:
            with uproot.open(filename) as f:
                events = f["Events"]

                HLTJet = ak.zip({
                    "IsoMu24": events["HLT_IsoMu24"].array(),
                    "IsoMu27": events["HLT_IsoMu27"].array()
                })
                if "HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5" in events.keys() and "HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5_TriplePFJet" in events.keys():
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5"].array()            , where="pt105")
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5_TriplePFJet"].array(), where="pt105triple")

                if "HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0"  in events.keys() and "HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0_TriplePFJet"  in events.keys():
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0"].array()            , where="pt125")
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0_TriplePFJet"].array(), where="pt125triple")

                if "HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85" in events.keys() and "HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85_TriplePFJet" in events.keys():
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85"].array()            , where="pt75")
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85_TriplePFJet"].array(), where="pt75triple")
                
                if "HLT_VBF_DiPFJet80_45_Mjj500_Detajj2p5_PFMET85" in events.keys() and "HLT_VBF_DiPFJet80_45_Mjj500_Detajj2p5_PFMET85_TriplePFJet" in events.keys():
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet80_45_Mjj500_Detajj2p5_PFMET85"].array()            , where="pt80")
                    HLTJet = ak.with_field(HLTJet, events["HLT_VBF_DiPFJet80_45_Mjj500_Detajj2p5_PFMET85_TriplePFJet"].array(), where="pt80_triple")
                
                if "HLT_DiJet110_35_Mjj650_PFMET110" in events.keys():
                    HLTJet = ak.with_field(HLTJet, events["HLT_DiJet110_35_Mjj650_PFMET110"].array(), where="pt110")

                OFFJet = vector.zip({
                    "pt"     : events["Jet_pt"].array(),
                    "eta"    : events["Jet_eta"].array(),
                    "phi"    : events["Jet_phi"].array(),
                    "mass"   : events["Jet_mass"].array(),
                    "nTracks": events["Jet_nConstituents"].array(),

                    "chEmEF": events["Jet_chEmEF"].array(),
                    "chHEF" : events["Jet_chHEF"].array(),
                    "neEmEF": events["Jet_neEmEF"].array(),
                    "neHEF" : events["Jet_neHEF"].array(),
                    "muEF"  : events["Jet_muEF"].array(),
                    "jetid" : events["Jet_jetId"].array()
                })

                MuonCollection = ak.zip({
                    "nMuon"    : events["nMuon"].array(),
                    "Muon_pt"  : events["Muon_pt"].array(),
                    "Muon_eta" : events["Muon_eta"].array(),
                    "Muon_phi" : events["Muon_phi"].array(),
                    "Muon_mass": events["Muon_mass"].array(),
                    "muRelIso" : events["Muon_pfRelIso04_all"].array()
                })

                TrigObj = ak.zip({
                    "id"        : events["TrigObj_id"].array(),
                    "filterBits": events["TrigObj_filterBits"].array(),
                    "pt"        : events["TrigObj_pt"].array(),
                    "eta"       : events["TrigObj_eta"].array(),
                    "phi"       : events["TrigObj_phi"].array(),
                    "nObj"      : events["nTrigObj"].array(),
                })

                METCollection = ak.zip({
                    "MET_pt" : events["MET_pt"].array(),
                    "MET_phi": events["MET_phi"].array(),
                })

                Luminosity = ak.zip({
                    "lum": events["luminosityBlock"].array(),
                    "run": events["run"].array()
                })

            OFFJets         = ak.concatenate((OFFJets, OFFJet))
            HLTJets         = ak.concatenate((HLTJets, HLTJet))
            MuonCollections = ak.concatenate((MuonCollections, MuonCollection))
            TrigObjs        = ak.concatenate((TrigObjs, TrigObj))
            METCollections  = ak.concatenate((METCollections, METCollection))
            Luminosities    = ak.concatenate((Luminosities, Luminosity))
        except (OSError, uproot.exceptions.KeyInFileError) as e: print(f"{filename} failed because of {e}. Skipping for now...")
    return OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections, Luminosities

def MakeVector(OFFJets, MuonCollections, METCollections=""):
    """
        This function converts an ak zipped object to vector zipped object. 
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
        "jetid": OFFJets.jetid
    })

    if len(METCollections):
        # Issue: prom*fb parquets do not have eta phi mass, but don't need to convert to vector, since MET(no-mu) calculation is not needed. Later, maybe remake the prom*fb HLTJets files.
        MuonCollections = vector.zip({
            "nMuon": MuonCollections.nMuon,
            "pt": MuonCollections.Muon_pt,
            "eta": MuonCollections.Muon_eta,
            "phi": MuonCollections.Muon_phi,
            "mass": MuonCollections.Muon_mass,
            "muRelIso": MuonCollections.muRelIso
        })

        METCollections = vector.zip({
            "pt": METCollections.MET_pt,
            "phi": METCollections.MET_phi
        })

    else:
        MuonCollections = ak.zip({
        "nMuon": MuonCollections.nMuon,
        "pt": MuonCollections.Muon_pt,
        "muRelIso": MuonCollections.muRelIso
    })
    return OFFJets, MuonCollections, METCollections

def LoadObjects(datapath, subset=""):
    if not any("METCollection" in f for f in os.listdir(datapath)): 
        OFFJets, MuonCollections = MakeVector(ak.from_parquet(f"{datapath}*OFFJets{subset}*.parquet"), ak.from_parquet(f"{datapath}*MuonCollections{subset}*.parquet"))[:2]
        METCollections  = ak.zip({"placeholder": [None]*len(OFFJets)})
    else: 
        OFFJets, MuonCollections, METCollections = MakeVector(ak.from_parquet(f"{datapath}*OFFJets{subset}*.parquet"), ak.from_parquet(f"{datapath}*MuonCollections{subset}*.parquet"), ak.from_parquet(f"{datapath}*METCollections{subset}*.parquet"))
    
    HLTJets         = ak.from_parquet(f"{datapath}*HLTJets{subset}*.parquet")
    TrigObjs        = ak.from_parquet(f"{datapath}*TrigObjs{subset}*.parquet")
    Luminosities    = ak.from_parquet(f"{datapath}*Luminosities{subset}*.parquet")
    print(f"Object loading done! nEvents: {len(OFFJets)}")
    return OFFJets, HLTJets, MuonCollections, TrigObjs, Luminosities, METCollections

def GetTriggerDict(triggerpath, analysis, tightcuts):
    """
        This function returns a dictionary of trigger path selection values.
    """
    if triggerpath=="pt105": # HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5(_TriplePFJet)
        triggerdict = {
            "leadjetpt": 105,
            "subleadjetpt": 40,
            "mjj": 1000,
            "deta": 3.5,
            "chEmEF": 0.99,
            "chHEF": 0.2,
            "neEmEF": 0.99,
            "neHEF": 0.9,
            "muonpt": 27,
            "muRelIso": 0.2
            # LLR CUTS:
            # "chHEF": 0.0, 0.3
            # "muonpt": 30,
        }
        if tightcuts=="tight":
            if analysis!="leadpt"   : triggerdict.update({"leadjetpt": 130}) # LLR: 125
            if analysis!="subleadpt": triggerdict.update({"subleadjetpt": 60}) # LLR: 50
            if analysis!="mjj"      : triggerdict.update({"mjj": 1300}) # LLR: 1300
            if analysis!="deta"     : triggerdict.update({"deta": 3.7}) # LLR: 4.0

    elif triggerpath=="pt125": # HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0(_TriplePFJet)
        triggerdict = {
            "leadjetpt": 125,
            "subleadjetpt": 45,
            "mjj": 720,
            "deta": 3.0,
            "chEmEF": 0.99,
            "chHEF": 0.3,
            "neEmEF": 0.99,
            "neHEF": 0.9,
            "muonpt": 27,
            "muRelIso": 0.2
        }
        if tightcuts=="tight":
            # to be determined
            if analysis!="leadpt"   : triggerdict.update({"leadjetpt": 130})
            if analysis!="subleadpt": triggerdict.update({"subleadjetpt": 60})
            if analysis!="mjj"      : triggerdict.update({"mjj": 1300})
            if analysis!="deta"     : triggerdict.update({"deta": 3.7})

    elif triggerpath=="pt75": # HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85(_TriplePFJet)
        triggerdict = {
            "leadjetpt": 75,
            "subleadjetpt": 40,
            "mjj": 500,
            "deta": 2.5,
            "MET": 85,
            "chEmEF": 0.99,
            "chHEF": 0.3,
            "neEmEF": 0.99,
            "neHEF": 0.9,
            "muonpt": 30,
            "muRelIso": 0.2
        }
        if tightcuts=="tight":
            if analysis!="leadpt"   : triggerdict.update({"leadjetpt": 85})
            if analysis!="subleadpt": triggerdict.update({"subleadjetpt": 50})
            if analysis!="mjj"      : triggerdict.update({"mjj": 550})
            if analysis!="deta"     : triggerdict.update({"deta": 3.5})
            if analysis!="met"      : triggerdict.update({"MET": 200})

    elif triggerpath=="pt80": # HLT_VBF_DiPFJet80_45_Mjj500_Detajj2p5_PFMET85(_TriplePFJet)
        triggerdict = {
            "leadjetpt": 80,
            "subleadjetpt": 45,
            "mjj": 500,
            "deta": 2.5,
            "MET": 85,
            "chEmEF": 0.99,
            "chHEF": 0.3,
            "neEmEF": 0.99,
            "neHEF": 0.9,
            "muonpt": 30,
            "muRelIso": 0.2
        }
        if tightcuts=="tight":
            if analysis!="leadpt"   : triggerdict.update({"leadjetpt": 85})
            if analysis!="subleadpt": triggerdict.update({"subleadjetpt": 50})
            if analysis!="mjj"      : triggerdict.update({"mjj": 550})
            if analysis!="deta"     : triggerdict.update({"deta": 3.5})
            if analysis!="met"      : triggerdict.update({"MET": 200})

    elif triggerpath=="pt110": # HLT_DiJet110_35_Mjj650_PFMET110
        triggerdict = {
            "leadjetpt": 110,
            "subleadjetpt": 35,
            "mjj": 650,
            "deta": 0,
            "MET": 110,
            "chEmEF": 0.99,
            "chHEF": 0.3,
            "neEmEF": 0.99,
            "neHEF": 0.9,
            "muonpt": 30,
            "muRelIso": 0.2
        }
        if tightcuts=="tight":
            if analysis!="leadpt"   : triggerdict.update({"leadjetpt": 85})
            if analysis!="subleadpt": triggerdict.update({"subleadjetpt": 50})
            if analysis!="mjj"      : triggerdict.update({"mjj": 550})
            if analysis!="deta"     : triggerdict.update({"deta": 3.5})
            if analysis!="met"      : triggerdict.update({"MET": 200})
    return triggerdict

def PrintCuts(cutfunc):
    """
        This decorator function prints the number of quantities (events, jets, or combinations of jets) before and after the function is executed.
    """
    if cutfunc.__name__=="DoCuts":
        def printer(*args, **kwargs):
            result = cutfunc(args[0][0], **kwargs)
            if len(kwargs.keys())==1: 
                idx = next((i for i, item in enumerate(result) if len(item) > 0), None)
                if "MET" in list(kwargs.keys())[0]: print(f"Number of {list(kwargs.keys())[0]} after {args[0][1]}: {len(result[idx])}")
                else: print(f"Number of {list(kwargs.keys())[0]} after {args[0][1]}: {ak.sum(ak.num(result[idx]))}")
            else: print(f"Number of events after {args[0][1]}: {len(result[0])}")
            return result
    else:
        def printer(*args, **kwargs):
            print(f"\n----------Starting {cutfunc.__name__}----------")
            print(f"Number of events before {cutfunc.__name__}: {len(args[0])}")
            result = cutfunc(*args, **kwargs)
            print(f"Number of events after {cutfunc.__name__}: {len(result[0])}")
            print(f"----------Finished {cutfunc.__name__}----------\n")
            return result
    return printer

@PrintCuts
def DoCuts(cut, OFFJets="", HLTJets="", MuonCollections="", TrigObjs="", METCollections="", JetCombo=""):
    # Should manually choose which ones to return when the function is called.
    """
        This function accepts one or more object(s) and make cuts.
        The scope of cutting (event-wise, jet-wise, or jetpair-wise) is built-in inside the cut input.
        When the function is called, use placeholders to simplify the retrieval.
    """
    if len(OFFJets)        : OFFJets = OFFJets[cut]
    if len(HLTJets)        : HLTJets = HLTJets[cut]
    if len(MuonCollections): MuonCollections = MuonCollections[cut]
    if len(TrigObjs)       : TrigObjs = TrigObjs[cut]
    if len(METCollections) : METCollections = METCollections[cut]
    if len(JetCombo)       : JetCombo = JetCombo[cut]
    return OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections, JetCombo

@PrintCuts
def MakeGolden(OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections, Luminosities, goldenpath):
    """
        This function cuts the events that are not in golden luminosity blocks, and returns the cut objects.
    """
    goldenJSON = json.load(open(goldenpath, 'r'))

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
    OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections = DoCuts([goldencut,"goldencut"], OFFJets=OFFJets, HLTJets=HLTJets, MuonCollections=MuonCollections, TrigObjs=TrigObjs, METCollections=METCollections)[:5]

    return OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections

@PrintCuts
def ApplyBasicCuts(OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections, analysis, triggerdict):
    print(f"Number of OFFJets before jetID cuts: {ak.sum(ak.num(OFFJets))}")

    jetidCut = ak.where(OFFJets.jetid>=2, True, False)
    OFFJets = DoCuts([jetidCut,"jetidCut"], OFFJets=OFFJets)[0]

    if (analysis!="leadchEmEF") and (analysis!="subleadchEmEF"):
        de, ef = (abs(OFFJets.eta) < 2.4), (triggerdict["chEmEF"] > OFFJets.chEmEF)
        chEmEFCut = (de & ef) | (~de & ef) | (~de & ~ef)
        OFFJets = DoCuts([chEmEFCut, "chEmEFCut"], OFFJets=OFFJets)[0]

    if (analysis!="leadchHEF") and (analysis!="subleadchHEF"):
        de, ef = (abs(OFFJets.eta) < 2.4), (triggerdict["chHEF"] < OFFJets.chHEF)
        chHEFCut = (de & ef) | (~de & ef) | (~de & ~ef)
        OFFJets = DoCuts([chHEFCut, "chHEFCut"], OFFJets=OFFJets)[0]

    if (analysis!="leadneEmEF") and (analysis!="subleadneEmEF"):
        de, ef = (abs(OFFJets.eta) < 2.4), (triggerdict["neEmEF"] > OFFJets.neEmEF)
        neEmEFCut = (de & ef) | (~de & ef) | (~de & ~ef)
        OFFJets = DoCuts([neEmEFCut, "neEmEFCut"], OFFJets=OFFJets)[0]

    if (analysis!="leadneHEF") and (analysis!="subleadneHEF"):
        de, ef = (abs(OFFJets.eta) < 2.4), (triggerdict["neHEF"] > OFFJets.neHEF)
        neHEFCut = (de & ef) | (~de & ef) | (~de & ~ef)
        OFFJets = DoCuts([neHEFCut, "neHEFCut"], OFFJets=OFFJets)[0]

    nJetCut = (ak.num(OFFJets)>=2)
    OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections = DoCuts([nJetCut, "nJetCut"], OFFJets=OFFJets, HLTJets=HLTJets, MuonCollections=MuonCollections, TrigObjs=TrigObjs, METCollections=METCollections)[:5]

    MuonCuts = (ak.any((MuonCollections.pt>=triggerdict["muonpt"]) & (MuonCollections.muRelIso<triggerdict["muRelIso"]), axis=1))
    OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections = DoCuts([MuonCuts, "MuonCuts"], OFFJets=OFFJets, HLTJets=HLTJets, MuonCollections=MuonCollections, TrigObjs=TrigObjs, METCollections=METCollections)[:5]

    if "IsoMu24" in HLTJets.fields:
        IsoMu24Cut = HLTJets.IsoMu24
        OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections = DoCuts([IsoMu24Cut,"IsoMu24Cut"], OFFJets=OFFJets, HLTJets=HLTJets, MuonCollections=MuonCollections, TrigObjs=TrigObjs, METCollections=METCollections)[:5]

    #elif "IsoMu27" in HLTJets.fields:
    #    IsoMu27Cut = HLTJets.IsoMu27
    #    OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections = DoCuts([IsoMu27Cut,"IsoMu27Cut"], OFFJets=OFFJets, HLTJets=HLTJets, MuonCollections=MuonCollections, TrigObjs=TrigObjs, METCollections=METCollections)[:5]

    if "rho" in METCollections.fields:
        METpt_nomu = np.sqrt((ak.sum(MuonCollections.px, axis=1) + METCollections.px)**2 + (ak.sum(MuonCollections.py, axis=1) + METCollections.py)**2)
        METCollections = ak.with_field(METCollections, METpt_nomu, "METpt_nomu")
        if analysis !="METAnalysis":
            METCut = METCollections.METpt_nomu > triggerdict["MET"]
            OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections = DoCuts([METCut, "METCut"], OFFJets=OFFJets, HLTJets=HLTJets, MuonCollections=MuonCollections, TrigObjs=TrigObjs, METCollections=METCollections)[:5]
            print(f"number of events after METCut: {format(len(OFFJets))}")

    return OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections

@PrintCuts
def AssignFilterBitsToOFFJets(OFFJets, HLTJets, TrigObjs, METCollections, filterbits):
    """
        This function makes cuts on TrigObjs, matches jets in TrigObj to OFFJets, and assigns the filterBits to OFFJets.
    """
    if filterbits:
        # selecting jets from TrigObjs
        PickJetsCut = ak.where(TrigObjs.id==1, True, False)
        TrigObjs = DoCuts([PickJetsCut, "PickJetsCut"], TrigObjs=TrigObjs)[3] # jetwise cut

        # selecting TrigObjs jets that pass HLT VBF filterBits
        rightmostbit = (TrigObjs.filterBits) & (-1*TrigObjs.filterBits)
        PassHLTVBFfBCut = (rightmostbit==1)|(rightmostbit==2)
        TrigObjs = DoCuts([PassHLTVBFfBCut, "PassHLTVBFfBCut"], TrigObjs=TrigObjs)[3]

        # discarding the events in TrigObjs with no passing jets
        ExistTrigObjsCut = ak.where(ak.num(TrigObjs)>0, True, False)
        OFFJets, HLTJets, mu_placeholder, TrigObjs, METCollections = DoCuts([ExistTrigObjsCut, "ExistTrigObjsCut"], OFFJets=OFFJets, HLTJets=HLTJets, TrigObjs=TrigObjs, METCollections=METCollections)[:5]

        # Making trig-off combos
        TrigOFFcombo = ak.cartesian({"tri": TrigObjs, "off": OFFJets[:,np.newaxis]})
        dR = np.sqrt((TrigOFFcombo.tri.eta-TrigOFFcombo.off.eta)**2 + (TrigOFFcombo.tri.phi-TrigOFFcombo.off.phi)**2)

        # calculating minimum deltaR
        mindR = ak.min(dR,axis=-1)
        dropTrigObj = ak.where(mindR>0.1,False,True)
        TrigObjs = DoCuts([dropTrigObj, "dropTrigObj"], TrigObjs=TrigObjs)[3]
        dR = dR[dropTrigObj]

        # discarding events with no matching jets
        NoTrigObjCut = ak.where(ak.num(TrigObjs)==0,False,True)
        OFFJets, HLTJets, mu_placeholder, TrigObjs, METCollections = DoCuts([NoTrigObjCut, "NoTrigObjCut"], OFFJets=OFFJets, HLTJets=HLTJets, TrigObjs=TrigObjs, METCollections=METCollections)[:5]
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
        JetPassedHLT = ak.where(filterBitsToAdd>0, True, False)

        # assigning filterBits and masking values to OFFJets
        OFFJets = ak.with_field(OFFJets, filterBitsToAdd ,"filterBits")
        OFFJets = ak.with_field(OFFJets, JetPassedHLT ,"JetPassedHLT")

        print("Successfully assigned the filterBits to offline jets!\n")
        return OFFJets, HLTJets, TrigObjs, METCollections
    
    else:
        print("filterbits is disabled for this analysis. Returning the original inputs.")
        return OFFJets, HLTJets, TrigObjs, METCollections
    
@PrintCuts
def ApplyTriggerCuts(OFFJets, HLTJets, TrigObjs, METCollections, analysis, triggerdict):
    OFFcombo = ak.combinations(OFFJets,2, fields=["jet1","jet2"])
    print("number of JetCombo before cuts: ", ak.count_nonzero(OFFcombo.jet1.pt))

    if analysis!="leadpt":
        leadjetptcut = (OFFcombo.jet1.pt>=triggerdict["leadjetpt"])
        OFFcombo = DoCuts([leadjetptcut, "leadjetptcut"], JetCombo=OFFcombo)[-1]

    if analysis!="subleadpt":
        subleadjetptcut = (OFFcombo.jet2.pt>=triggerdict["subleadjetpt"])
        OFFcombo = DoCuts([subleadjetptcut,"subleadjetptcut"], JetCombo=OFFcombo)[-1]

    if analysis!="mjj":
        jjsum  = OFFcombo.jet1 + OFFcombo.jet2
        mjjcut = (jjsum.mass>=triggerdict["mjj"])
        OFFcombo = DoCuts([mjjcut, "mjjcut"], JetCombo=OFFcombo)[-1]

    if analysis!="deta":
        detas = abs(vector.Spatial.deltaeta(OFFcombo.jet1, OFFcombo.jet2))
        detacut = (detas >= triggerdict["deta"])
        OFFcombo = DoCuts([detacut, "detacut"], JetCombo=OFFcombo)[-1]

    eventcut = ak.where(ak.num(OFFcombo)>0,True, False)
    OFFJets, HLTJets, mu_placeholder, TrigObjs, METCollections, OFFcombo = DoCuts([eventcut, "eventcut"], OFFJets=OFFJets, HLTJets=HLTJets, TrigObjs=TrigObjs, METCollections=METCollections, JetCombo=OFFcombo)
    return OFFJets, HLTJets, TrigObjs, METCollections, OFFcombo

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

@PrintCuts
def GetNumDenom(shouldPassHLT_Jets, HLTJets, METCollections, OFFcombo, analysis, triggerpath, filterbits):
    jjsum = OFFcombo.jet1 + OFFcombo.jet2
    maxmjjidx = ak.Array(list(ak.unflatten(ak.argmax(jjsum.mass,axis=1),1)))
    shouldPass_OFFcombo = OFFcombo[maxmjjidx] # denominator

    if   triggerpath=="pt105": HLTCut = [HLTJets.pt105|HLTJets.pt105triple][0]
    elif triggerpath=="pt125": HLTCut = [HLTJets.pt125|HLTJets.pt125triple][0]
    elif triggerpath=="pt75" : HLTCut = [HLTJets.pt75|HLTJets.pt75triple][0]
    elif triggerpath=="pt80" : HLTCut = [HLTJets.pt80|HLTJets.pt80triple][0]
    elif triggerpath=="pt110": HLTCut = [HLTJets.pt110][0]

    trigPassed_OFFcombo = DoCuts([HLTCut, "HLTCut"], JetCombo=shouldPass_OFFcombo)[5] # numerator

    if analysis=="leadpt": 
        return ak.flatten(shouldPass_OFFcombo.jet1.pt), ak.flatten(trigPassed_OFFcombo.jet1.pt)
    elif analysis=="mjj":
        shouldPass_jjsum = shouldPass_OFFcombo.jet1 + shouldPass_OFFcombo.jet2
        trigPassed_jjsum = trigPassed_OFFcombo.jet1 + trigPassed_OFFcombo.jet2
        return ak.flatten(shouldPass_jjsum.mass), ak.flatten(trigPassed_jjsum.mass)
    elif analysis=="deta":
        shouldPass_deta = vector.Spatial.deltaeta(shouldPass_OFFcombo.jet1, shouldPass_OFFcombo.jet2)
        trigPassed_deta = vector.Spatial.deltaeta(trigPassed_OFFcombo.jet1, trigPassed_OFFcombo.jet2)
        return ak.flatten(shouldPass_deta), ak.flatten(trigPassed_deta)


"""
@PrintCuts
def GetNumDenom(shouldPassHLT_Jets, HLTJets, METCollections, OFFcombo, analysis, triggerpath, filterbits):
    if   triggerpath=="pt105": HLTCut = [HLTJets.pt105|HLTJets.pt105triple][0]
    elif triggerpath=="pt125": HLTCut = [HLTJets.pt125|HLTJets.pt125triple][0]
    elif triggerpath=="pt75" : HLTCut = [HLTJets.pt75|HLTJets.pt75triple][0]
    elif triggerpath=="pt80" : HLTCut = [HLTJets.pt80|HLTJets.pt80triple][0]
    elif triggerpath=="pt110": HLTCut = [HLTJets.pt110][0]

    if "pt" in analysis or "EF" in analysis:
        trigpassed_OFFcombo = DoCuts([HLTCut, "HLTCut"], JetCombo=OFFcombo)[5]

        if filterbits:
            # selecting jets that passed VBF HLT trigger
            combofbcut = trigpassed_OFFcombo.jet1.JetPassedHLT & trigpassed_OFFcombo.jet2.JetPassedHLT
            fbpassed_OFFcombo = DoCuts([combofbcut, "combofbcut"], JetCombo=trigpassed_OFFcombo)[5]
            nocombocut = ak.where(ak.num(fbpassed_OFFcombo)>0, True, False)
            passed_OFFcombo = DoCuts([nocombocut, "nocombocut"], JetCombo=fbpassed_OFFcombo)[5]
        else:
            passed_OFFcombo = trigpassed_OFFcombo
            passed_OFFJets = trigpassed_OFFcombo.jet1

        if   analysis=="leadpt"       : return ak.flatten(OFFcombo.jet1.pt), ak.flatten(passed_OFFcombo.jet1.pt)
        elif analysis=="subleadpt"    : return ak.flatten(OFFcombo.jet2.pt), ak.flatten(passed_OFFcombo.jet2.pt)

        elif analysis=="leadchEmEF"   : return shouldPassHLT_Jets.chEmEF[:,0], passed_OFFJets.chEmEF[:,0]
        elif analysis=="leadchHEF"    : return shouldPassHLT_Jets.chHEF[:,0] , passed_OFFJets.chHEF[:,0]
        elif analysis=="leadneEmEF"   : return shouldPassHLT_Jets.neEmEF[:,0], passed_OFFJets.neEmEF[:,0]
        elif analysis=="leadneHEF"    : return shouldPassHLT_Jets.neHEF[:,0] , passed_OFFJets.neHEF[:,0]
        elif analysis=="leadmuEF"     : return shouldPassHLT_Jets.muEF[:,0]  , passed_OFFJets.muEF[:,0]

        elif analysis=="subleadchEmEF": return shouldPassHLT_Jets.chEmEF[:,1], passed_OFFJets.chEmEF[:,1]
        elif analysis=="subleadchHEF" : return shouldPassHLT_Jets.chHEF[:,1] , passed_OFFJets.chHEF[:,1]
        elif analysis=="subleadneEmEF": return shouldPassHLT_Jets.neEmEF[:,1], passed_OFFJets.neEmEF[:,1]
        elif analysis=="subleadneHEF" : return shouldPassHLT_Jets.neHEF[:,1] , passed_OFFJets.neHEF[:,1]
        elif analysis=="subleadmuEF"  : return shouldPassHLT_Jets.muEF[:,1]  , passed_OFFJets.muEF[:,1]
    
    elif "met" in analysis:
        shouldPass_METCollections = METCollections
        trigpassed_METCollections = DoCuts([HLTCut, "HLTCut"], METCollections=shouldPass_METCollections)[4]
        passed_METCollections = trigpassed_METCollections
        return shouldPass_METCollections.pt, passed_METCollections.pt
    
    elif "mjj" in analysis or "deta" in analysis:
        shouldPass_jjsum = OFFcombo.jet1 + OFFcombo.jet2
        shouldPass_mjj, shouldPass_deta = shouldPass_jjsum.mass, vector.Spatial.deltaeta(OFFcombo.jet1, OFFcombo.jet2)
        trigpassed_OFFcombo = DoCuts([HLTCut, "HLTCut"], JetCombo=OFFcombo)[5]
        if filterbits:
            fbcut = trigpassed_OFFcombo.jet1.JetPassedHLT & trigpassed_OFFcombo.jet2.JetPassedHLT
            fbpassed_combo_j1, fbpassed_combo_j2 = DoCuts([fbcut, "fbcut"], OFFJets=trigpassed_OFFcombo.jet1)[0], DoCuts([fbcut, "fbcut"], OFFJets=trigpassed_OFFcombo.jet2)[0]
            passed_jjsum = fbpassed_combo_j1 + fbpassed_combo_j2
            passed_mjj   = passed_jjsum.mass
            passed_deta  = vector.Spatial.deltaeta(fbpassed_combo_j1, fbpassed_combo_j2)
        else:
            passed_jjsum = trigpassed_OFFcombo.jet1 + trigpassed_OFFcombo.jet2
            passed_mjj   = passed_jjsum.mass
            passed_deta  = vector.Spatial.deltaeta(trigpassed_OFFcombo.jet1, trigpassed_OFFcombo.jet2)
        if   analysis=="mjj" : return ak.flatten(shouldPass_mjj) , ak.flatten(passed_mjj)
        elif analysis=="deta": return abs(ak.flatten(shouldPass_deta)), abs(ak.flatten(passed_deta))
"""
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer) : return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray) : return obj.tolist()
        return super(NpEncoder, self).default(obj)
    
### PLOTTING ###
def GetClopperPearsonInterval(hltPassed, total, alpha):
    min, max = beta.ppf(alpha, hltPassed, total - hltPassed + 1), beta.ppf(1 - alpha, hltPassed + 1, total - hltPassed)
    center = 0
    if total !=0: center = hltPassed/total
    min, max = center-min , max-center
    return min, max

def GetEfficiency(binsize, maxbin, HLTPassedQuantity, HLTCandQuantity):
    bincenters = np.arange(binsize,maxbin,2*binsize)
    effs = np.zeros(len(bincenters))
    errmin,errmax = np.zeros(len(bincenters)), np.zeros(len(bincenters))

    for i, c in enumerate(bincenters):
        minlim, maxlim = round(c - binsize,5), round(c + binsize,5)
        numerator = ak.count_nonzero(ak.where((HLTPassedQuantity>=minlim) & (HLTPassedQuantity<maxlim), 1, 0))
        denominator = ak.count_nonzero(ak.where((HLTCandQuantity   >=minlim) & (HLTCandQuantity   <maxlim), 1, 0))
        errmin[i],errmax[i] = GetClopperPearsonInterval(numerator,denominator,0.05)
        if denominator!=0: effs[i] = numerator/denominator
    yerrmin, yerrmax = np.nan_to_num(errmin), np.nan_to_num(errmax)

    return effs, yerrmin, yerrmax, bincenters

def GetVardict(numerator, denominator, analysis, triggerdict):
    if analysis=="leadpt":
        vardict = {
            "plotname": "leadpt",
            "binsize"  : 5,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 300,
            "xlabel": r"$p_T^{leadjet}$ [GeV]",
            "threshold": triggerdict["leadjetpt"],
        }

    if analysis=="subleadpt":
        vardict = {
            "plotname": "subleadpt",
            "binsize"  : 2,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 150,
            "xlabel": r"$p_T^{subleadjet}$ [GeV]",
            "threshold": triggerdict["subleadjetpt"],
        }

    if analysis=="mjj":
        vardict = {
            "plotname": "mjj",
            "binsize"  : 50,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 2500,
            "xlabel": r"$M_{jj}$ [GeV]",
            "threshold": triggerdict["mjj"],
        }

    if analysis=="deta":
        vardict = {
            "plotname": "deta",
            "binsize"  : 0.1,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 7,
            "xlabel": r"$\Delta\eta (j_1,j_2)$",
            "threshold": triggerdict["deta"],
        }

    if analysis=="leadchEmEF":
        vardict = {
            "plotname": "LeadJetchEmEF",
            "binsize"  : 0.025,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 1.0,
            "xlabel": "Leadjet chEmEF",
            "threshold": -999,
        }

    if analysis=="leadchHEF":
        vardict = {
            "plotname": "LeadJetchHEF",
            "binsize"  : 0.025,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 1.0,
            "xlabel": "Leadjet chHEF",
            "threshold": -999,
        }

    if analysis=="leadneEmEF":
        vardict = {
            "plotname": "LeadJetneEmEF",
            "binsize"  : 0.025,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 1.0,
            "xlabel": "Leadjet neEmEF",
            "threshold": -999,
        }

    if analysis=="leadneHEF":
        vardict = {
            "plotname": "LeadJetneHEF",
            "binsize"  : 0.025,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 1.0,
            "xlabel": "Leadjet neHEF",
            "threshold": -999,
        }
        
    if analysis=="leadmuEF":
        vardict = {
            "plotname": "LeadJetmuEF",
            "binsize"  : 0.025,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 1.0,
            "xlabel": "Leadjet muEF",
            "threshold": -999,
        }

    if analysis=="subleadchEmEF":
        vardict = {
            "plotname": "SubLeadJetchEmEF",
            "binsize"  : 0.025,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 1.0,
            "xlabel": "SubLeadJet chEmEF",
            "threshold": -999,
        }

    if analysis=="subleadchHEF":
        vardict = {
            "plotname": "SubLeadJetchHEF",
            "binsize"  : 0.025,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 1.0,
            "xlabel": "SubLeadJet chHEF",
            "threshold": -999,
        }

    if analysis=="subleadneEmEF":
        vardict = {
            "plotname": "SubLeadJetneEmEF",
            "binsize"  : 0.025,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 1.0,
            "xlabel": "SubLeadJet neEmEF",
            "threshold": -999,
        }

    if analysis=="subleadneHEF":
        vardict = {
            "plotname": "SubLeadJetneHEF",
            "binsize"  : 0.025,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 1.0,
            "xlabel": "SubLeadJet neHEF",
            "threshold": -999,
        }

    if analysis=="subleadmuEF":
        vardict = {
            "plotname": "SubLeadJetmuEF",
            "binsize"  : 0.025,
            "numerator": numerator,
            "denominator": denominator,
            "maxbin": 1.0,
            "xlabel": "SubLeadJet muEF",
            "threshold": -999,
        }
    return vardict

def GetEffDict(vardict, trigdict, effs, yerrmin, yerrmax, bincenters):
    effdict = {
        "vardict": vardict,
        "trigdict": trigdict,
        "effs": effs,
        "yerrmin": yerrmin,
        "yerrmax":yerrmax,
        "bincenters": bincenters
    }
    return effdict
