# 2023 VBF SUEP MC Production

Things that are included from the beginning:
- ```readme.md```
- ```./fragments/```
- ```CMSSW_setup.sh```
- ```config_setup.sh```
- ```configSetup.py```
- ```submitJobs.py```

Here are the steps to creating VBF SUEP 2023 Run3 MC samples. Make sure to deactivate any conda environment.
|Command|Description|
|-------|-----------|
|1. ```cd suep-production_2023```|- Moves to the working directory.<br>- Make sure that you are in ```el9``` os environment.|
|2. ```sh CMSSW_setup.sh```|- Installs appropriate CMSSW release (```CMSSW_13_0_14```).<br>- Adds required PhysicsTools packages to the CMSSW release.<br>- Copies the ```fragments``` directory to appropriate place in the CMSSW release.<br>- This step needs to be done only once.|
|3. ```cmsenv```|- Activates cms computing environment. Make sure this is run in ```CMSSW_13_0_14/src``` directory.|
|4. ```sh config_setup.sh```|- Runs ```configSetup.py``` script for all data tiers. <br>- Creates the config file templates (fragment needs to be added to ```gensim_template.py```, and customization options need to be added for all tiers) inside ```config_template``` directory.<br>- Creates finalized config files in ```config_final``` directory.<br>- <span style="color:#f44336">\*ATTENTION\*: </span>Configure the suep parameters (mass, decay mode, temperature, etc.) in ```config_setup.sh``` at this stage.|
|5. ```python3 submitJobs.py```|- Creates jobs to be sent to condor.<br>- Creates a ```submit.sub``` file for condor submission.<br>- If ```doSubmit=True```, then submits the jobs to condor.|