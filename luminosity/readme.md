 
# Notes on .txt files in luminosity directory (231023)

- ```2023all_lumiJson.txt``` contains the luminosity blocks for the following eight datasets:
    - ```/Muon[0-1]/Run2023C-PromptReco-v[3-4]/MINIAOD```, and
    - ```/Muon[0-1]/Run2023D-PromptReco-v[1-2]/MINIAOD```.

    This is to be used for brilcalc.

- ```2023all_luminosity.txt``` contains the total integrated luimnosity for the datasets used for Run3 VBF Trigger efficiency analysis.

- ```lumiJSON.py``` file is run by the following command: ```python lumiJSON.py --dataset={datasets} --outputdir={outputdir} --goldenpath={goldenpath}```. Here are some instructions for entering datasets.
    - ```--dataset``` argument can have three inputs: i) local directory(ies) that contain root files, ii) dataset(s) on DAS, and iii) local directory(ies) that contain ```*Luminosities*.parquet``` files.
    - When entering local directory(ies), the format is ```--dataset='/eos/.../','/eos/.../'```. Notice that comma separates the directories and there is no space between the comma. Each directory is embraced by single quatoation marks. This i s becuase the datasets are read with a comma delimiter. Also notice that each directory ends with a slash ```/```. 
    - When entering dataset(s) in DAS, the format is ```--dataset='dataset=*/*/*','dataset=*/*/*'```. Make sure that ```dataset=``` is included in the argument to i) mark that the dataset comes from DAS, and ii) make the code simpler without manually having to append the phrase when searching from DAS. The comma and single quotation marks follow the same rule and reason for local directories.
    - When entering directory(ies) to parquet files, same syntax is applied as to directories to local root files.
    - All types of arguments allow globbing. 