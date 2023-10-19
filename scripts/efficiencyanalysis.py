from optparse import OptionParser
import definitions as vbf
import json
import os

### PREPROCESSING ###
parser = OptionParser(usage="%prog [options]")
parser.add_option("--triggerpath", dest="triggerpath", default="pt105"          , help="options: pt105, pt125, pt75, pt80, pt110. More info here")
parser.add_option("--analysis"   , dest="analysis"   , default="mjj"            , help="variable to analyze. x-axis in efficiency plot. Options are available here")
parser.add_option("--tightcuts"  , dest="tightcuts"  , default=""               , help="'loose' or 'tight'")
parser.add_option("--filterbits" , dest="filterbits" , default=False            , help="If true, filterbits are considered. If not, just the triggerpath")
parser.add_option("--goldenpath" , dest="goldenpath" , default="2023golden.json", help="path for goldenJSON file.")
parser.add_option("--dataset"    , dest="dataset"    , default="promC0v3fb"     , help="format: [reco][era]v[version][filterBits]. Directory for parquetpath.")
parser.add_option("--outputdir"  , dest="outputdir"  , default="./"             , help="directory where the output json files will be stored")
parser.add_option("--subset"     , dest="subset"     , default=""               , help="Only loads subset of the dataset. String that specifies which files to load. options: '0000', '3600'...")
(options, args) = parser.parse_args()

triggerpath = options.triggerpath
analysis    = options.analysis
tightcuts   = options.tightcuts
filterbits  = options.filterbits
goldenpath  = options.goldenpath
dataset     = options.dataset
outputdir   = options.outputdir
subset      = options.subset

datapath    = f"/eos/user/j/jkil/SUEP/vbftrigger/datasets/parq/{dataset}_parq/"
outputjson  = f"{outputdir}{dataset}_{analysis}_{triggerpath}_{tightcuts}.json" 
triggerdict = vbf.GetTriggerDict(triggerpath, analysis, tightcuts)

### PROCESSING ###
if os.path.exists(outputjson) and os.path.getsize(outputjson)>1000:
    print(f"json: {outputjson}")
    print("Good quality json already exists! Terminating the analyzer.")
else:
    OFFJets, HLTJets, MuonCollections, TrigObjs, Luminosities, METCollections            = vbf.LoadObjects(datapath, subset=subset)
    goldOFFJets , goldHLTJets , goldMuonCollections , goldTrigObjs , goldMETCollections  = vbf.MakeGolden(OFFJets, HLTJets, MuonCollections, TrigObjs, METCollections, Luminosities, goldenpath)
    basicOFFJets, basicHLTJets, basicMuonCollections, basicTrigObjs, basicMETCollections = vbf.ApplyBasicCuts(goldOFFJets, goldHLTJets, goldMuonCollections, goldTrigObjs, goldMETCollections, analysis, triggerdict)
    assigned_OFFJets, assigned_HLTJets, assigned_TrigObjs, assigned_METCollections       = vbf.AssignFilterBitsToOFFJets(basicOFFJets, basicHLTJets, basicTrigObjs, basicMETCollections, filterbits)
    cleanOFFJets, cleanHLTJets, cleanTrigObjs, cleanMETCollections, cleanOFFcombo        = vbf.ApplyTriggerCuts(assigned_OFFJets, assigned_HLTJets, assigned_TrigObjs, assigned_METCollections, analysis, triggerdict)
    shouldPassHLT_OFFjets, shouldPassHLT_combo                                           = vbf.SelectHLTJetsCand(cleanOFFJets, cleanOFFcombo)
    shouldPassQuantity, passedQuantity                                                   = vbf.GetNumDenom(shouldPassHLT_OFFjets, cleanHLTJets, cleanMETCollections, shouldPassHLT_combo, analysis, triggerpath, filterbits)

    ### POSTPROCESSING ###
    quantity_dict = {
        "dataset"    : dataset,
        "analysis"   : analysis,
        "numerator"  : list(passedQuantity),
        "denominator": list(shouldPassQuantity)
    }
    #with open(outputjson, 'w') as f: json.dump(quantity_dict, f, cls=vbf.NpEncoder, indent=4)
    print(f"{outputdir}{dataset}_{analysis}_{triggerpath}_{tightcuts}.json created!")