# Scripts
## Raymond Kil, 2023

# Script Descriptions
## definitions.py
This script contains the functions that are used for the efficiency analysis. The functions include:
- producing of parquet files
- making cuts
- assigning filterBits from trigger objects to offline jets
- calculating the efficiency

## efficiencyanalysis.py
This script takes in the parquet files of a dataset and produces a JSON file that contains the numerator and denominator for efficiency calculation. The arguments are described below.
|argument|description|
|---------------|----------|
|```triggerpath```|Triggerpath to test. Enter one among the old MET prompt trigger path (```pt110```), the new parking MET trigger path (```pt75```, or ```pt80```), or the new inclusive trigger path (```pt105```, or ```pt125```). The keys and corresponding exact trigger path names are described in the ```readme.md``` file for the project.|
|```analysis```|The figure of merit to measure the efficiency. This variable is the x-axis for the efficiency plot. Trigger-specific cuts are made except for this variable. Possible options are ```leadpt, subleadpt, mjj, deta, met, ```|
|```tightcuts```|Whether to apply tight selections or loose selections to the data. Options are ```loose``` and ```tight```. Loose cuts corresponds to the baseline cuts specified by the trigger path. Tight cuts are selected to ensure that the data is at the plateau with respect to other variables, so that the shapes of turn on and plateau are not affected by other variables. The numeric values for tight cuts are selected by inspecing the efficiency plots with loose selection criteria.|
|```filterbits```|Jet-level Boolean that indicates whether a jet passed VBF HLT or not. Options: ```True```, ```False```|
|```goldenpath```|Path to the ```2023golden.json``` file. This is used for selecting the golden events.|
|```dataset```|The compact name of the dataset. Ex) ```promC0v3```.|
|```outputdir```|Directory of which the output JSON is to be located. |
|```subset```|This option enables the JSON production with only a subset of data. This is |

## makeobjects.py
This script makes parquet files out of nanoaod files.
The input is a text file containing the file names of a dataset. The nanoaod files can either be in DAS or local directory. The output are the parquet files that contain only the relevant information from nanoaod files for this analysis. The names of the parquet files are written in the following format:

```{prom/park}{C/D}{0,1,2...}v{1,2,3,4}{ObjectName}{aodFileRange}-{aodFileRange}.parquet```

The list of arguments are described below:
|argument|description|
|---------------|----------|
|```filenames```|This is the path to the .txt file that contains the list of nanoaod file names. Each file name is separated by a newline. If the file names start with ```/store/```, then the program knows that the corresponding nanoaod file(s) are located in DAS. If the file names start with ```/eos/```, then the files are in the local directory.|
|```parqpath```|This is the path to the directory where the produced parquet files will be placed. Make sure to end the path with a slash ```/```.|
|```dataset```|This is a string that specifies the dataset of which the nanoaod files are from. This string is placed in front of the parquet files to specify the dataset. For example, ```parkC0v3_OFFJets```For more detail on how the datasets are named, please consult the ```readme.md``` in the project description page.|
|```nparq```|The maximum number of nanoaod files to be included in one parquet file. For example, if there are 450 nanoaod files and nparq=200, then two parquet files will be made for each object, one containing 0th-199th nanoaod file, and the other containing 200th-449th nanoaod files.|

Remember to enable the proxy. If the code is executed interactively, simply use ```voms-proxy-init -voms cms -rfc```. If submitting condor jobs, use ```voms-proxy-init -voms cms --rfc -valid 192:00 --out {proxyDir}x509up_u146772``` in the Terminal window of which condor jobs will be sent.

## plotefficiency.py
This script takes in the JSON files that contains the numerators and denominators thta were produced from ```efficiencyanalysis.py``` script, calculates the trigger efficiency per bin, and plots the efficiency as a function of a variable. The arguments are described below.
|argument|description|
|---------------|----------|
|```triggerpath```|Equivalent to above.|
|```analysis```|Equivalent to above.|
|```tightcuts```|Equivalent to above.|
|```outputdir```||
|```effoutdir```||
|```shape```||
|```jsonpath```|Path to where the numerator/denominator JSON files are located. ***Note that this is a path to where the JSON "directories" are located, not a specific directory that contains the JSON files. |
|```compare```|Enabling this option draws multiple plots on single canvas, according to the comparing criteria. The options are ```pp``` (prompt vs. parking), ```cd``` (dataset C vs. dataset D), and ```tl```(tightcuts vs. loosecuts). |

```
vbftrigger/
├─ datasets/
│  ├─ nano/
│  │  ├─ parkC0v3/
│  │  ├─ ...
│  │  ├─ promC0v3/
│  │  │  ├─ nanoaod_0000.root
│  │  │  ├─ ...
│  │  │  ├─ nanoaod_0420.root
│  │  └─ ...
│  ├─ parq/
│  │  ├─ parkC0v3/
│  │  ├─ .../
│  │  ├─ promC0v3/
│  │  │  ├─ promC0v3_HLTJets0000-0199.parquet
│  │  │  ├─ promC0v3_Luminosities0000-0199.parquet
│  │  │  ├─ promC0v3_METCollections0000-0199.parquet
│  │  │  ├─ promC0v3_MuonCollections0000-0199.parquet
│  │  │  ├─ promC0v3_OFFJets0000-0199.parquet
│  │  │  ├─ promC0v3_TrigObjs0000-0199.parquet
│  │  │  ├─ ...
│  │  │  ├─ promC0v3_HLTJets0400-0420.parquet
│  │  │  └─ ...
│  │  └─ .../
│  └─ json/
│     ├─ parkC0v3/
│     │  ├─ promC0v3fb_leadpt_pt105_loose.json
│     │  ├─ promC0v3fb_leadpt_pt105_tight.json
│     │  ├─ promC0v3fb_mjj_pt105_loose.json
│     │  └─ ...
│     └─ .../
├─ scripts/
``` 




230918

Here is an expanded note about SelectHLTJetsCand function.

# Reshaping Jets 
  # Originally, Jets for each event is single array of jets like: [[201, 69, 60.9],...]
  # exp_OFFJets_pt returns duplicates of the set of jets to match OFFcombo.
  # If OFFcombo.jet1[num], OFFcombo.jet1[num] = [201, 201], [69, 60.9], then exp_OFFJets_pt is [[201, 69, 60.9], [201, 69, 60.9]].
  # exp_OFFcombo_jet1 == OFFcombo.jet1. This does not change.

# Masking OFFcombo jets in Jets
  # jet1mask masks the leadjets in the broadcasted exp_OFFJets_pt format. Ex) [[201, 69, 60.9], [201, 69, 60.9]] -> [[True, False, False], [True, False, False]]
  # Similar with jet2mask, selects the subleadjet.                        Ex) [[201, 69, 60.9], [201, 69, 60.9]] -> [[False, True, False], [False, False, True]]

230925
The vbftrigger directory is now organized in the following way:
```
vbftrigger/
├─ vbftrigger/
│  ├─ scripts/
│  │ ├─ __init__.py
│  │ ├─ definitions.py
│  ├─ efficiency_analysis/
│  │ ├─ efficiencyanalysis.py
└──── validation/
```
Now when I execute a script that is NOT in scripts directory (say, in efficiency_analysis) that imports scripts from scripts, the commandline looks like: python -m vbftrigger.efficiency_analysis.efficiencyanalysis from the directory /eos/user/j/jkil/SUEP/vbftrigger

