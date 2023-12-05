# VBF Trigger

## Analyzer
Analyzer is divided into three parts: i) **nanoaod production & organization**, ii) **efficiency analysis**, and iii) **plotting**. There are scripts dedicated for each step
efficiencyanalysis.py, and efficiencyplotting.py.

## Datasets
The datasets analyzed in this project are produced in the Summer of 2023.
Two quantities that divide the datasets are **era** and **reconstruction chain**.
- **era**: the segments in data taking. Among Summer 2023 datasets, eras _C_ and _D_ contain the trigger paths of interest, namely, ```HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5(_TriplePFJet)``` and ```HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0(_TriplePFJet)```.
- **reconstruction chain**: type of object reconstruction. Two types of the reconstruction chain used in the datasets of interest are _prompt_ and _parking_. 

### FilterBits
FilterBits is a quantity that specifies if individual reconstructed object passed a specific trigger path. In the analysis, filterBits is used as another benchmark along with trigger path to calculate the efficiency.

### Labeling
The datasets are compactly labeled by specifying the era, reconstruction chain, and the inclusion of filterBits in the format of ```[reco][era][filterbit]_[extension]```. For example, the dataset ``` /Muon0/Run2023C-PromptReco-v4/MINIAOD``` is labeled as **promC0v4_mini**. Extensions are in formats miniaod (mini), nanoaod (nano), parquet (parq), or json (json). The workflow produces the files in the order specified. 


The triggerpaths being analyzed in the study are:
| Full Name | Compact Name |
| -------- | -------- |
| ```HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5```| pt105 |
|```HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5_TriplePFJet```|pt105triple|
|```HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0```|pt125|
|```HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0_TriplePFJet```|pt125triple|
|```HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85```|pt75|
|```HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85_TriplePFJet```|pt75triple|
|```HLT_VBF_DiPFJet80_45_Mjj500_Detajj2p5_PFMET85```|pt80|
|```HLT_VBF_DiPFJet80_45_Mjj500_Detajj2p5_PFMET85_TriplePFJet```|pt80triple|
|```HLT_DiJet110_35_Mjj650_PFMET110```|pt110|

json files are named as [reco][era]v[version]\_[analysis]\_[triggerpath]\_[tight]_[filterBits].json.

Available analyses are:
- leadpt
- subleadpt
- mjj
- deta
- met
- leadchEmEF
- leadchHEF
- leadneEmEF
- leadneHEF
- leadmuEF
- subleadchEmEF
- subleadchHEF
- subleadneEmEF
- subleadneHEF
- subleadmuEF

If you want to analyze different triggerpaths, you need to update the following:
- add the triggerdict in GetTriggerDict

The datasets are structured in the following way:
```
    vbftrigger/
    |-- scripts/
    |   |-- main/
    |   |-- test/
    |-- datasets/
    |   |-- nano/
    |   |-- parq/
    |   |-- json/
    |   |-- effs/

```

## Dependencies
- vector
- awkward array