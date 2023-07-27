"""
This program 
    1) creates job*.sh files for each command responsible for making NANOAOD files from the MINIAOD inputs,
    2) creates the submit.sub file responsible for queueing all job*.sh files, and
    3) submits the submit.sub file to HTCondor.
Currently, the program targets the creation of NANOAOD files corresponding to MINIAOD files in the following datasets, with jet-level triggerpath information:
'dataset=/Muon0/Run2023C-PromptReco-v4/MINIAOD' and 'dataset=/Muon1/Run2023C-PromptReco-v4/MINIAOD'.
The datasets are found here: https://cmsweb.cern.ch/das/
For more information on HTCondor, visit https://htcondor.readthedocs.io/en/latest/index.html.
Raymond Kil, 2023
"""

import numpy as np
import os

###### Making a list of all rootfile names ######
txtfilepath = "/eos/user/j/jkil/SUEP/suep-production/2023C_mu_NANOAOD_withJetFB/"
rootfilenames = []
with open(txtfilepath + "MuAll_2023C_MINIAOD.txt", 'r') as f:
    for line in f:
        rootfilenames.append(line.strip())
nCom = 100
slicing = np.arange(0,len(rootfilenames),nCom)

###### Specifying/Making Directories as Needed ######
pyDir       = "/eos/user/j/jkil/SUEP/suep-production/test/Run3Summer22EE/ReReco-Run2023_nanoaod.py"
nanoaodDir  = "/eos/user/j/jkil/SUEP/suep-production/2023C_mu_NANOAOD_withJetFB/NANOAOD/"
eoslogDir   = "/eos/user/j/jkil/SUEP/suep-production/2023C_mu_NANOAOD_withJetFB/eosbatchlogs/"
batchlogDir = "/afs/cern.ch/user/j/jkil/TEST/batchlogs/"
shfilesDir  = "/afs/cern.ch/user/j/jkil/TEST/exec/"
proxyDir    = "/afs/cern.ch/user/j/jkil/TEST/proxy/"

#condorlogDir = "/afs/cern.ch/user/j/jkil/TEST/"

if not os.path.exists(nanoaodDir) : os.system("mkdir {}".format(nanoaodDir))
if not os.path.exists(batchlogDir): os.system("mkdir {}".format(batchlogDir))
if not os.path.exists(eoslogDir)  : os.system("mkdir {}".format(eoslogDir))
if not os.path.exists(shfilesDir) : os.system("mkdir {}".format(shfilesDir))
if not os.path.exists(proxyDir)   : os.system("mkdir {}".format(proxyDir))

###### Making job.sh Files ######
os.system("voms-proxy-init -voms cms --rfc -valid 192:00 --out {}x509up_u146772".format(proxyDir))
for i, s in enumerate(slicing):
    batch = rootfilenames[s:s+nCom]
    with open("{}job_{}-{}.sh".format(shfilesDir, s, str(s+nCom-1)), 'w') as shf:
        shf.write("#!/bin/sh\n")
        shf.write("\n")
        shf.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
        shf.write("export X509_USER_PROXY={}x509up_u146772\n".format(proxyDir))
        shf.write("cd /eos/user/j/jkil/SUEP/suep-production/CMSSW_13_0_6/src/\n")
        shf.write("cmsenv\n")
        shf.write("cd -\n")
        shf.write("\n")
        for idx, line in enumerate(batch):
            shf.write(f"cmsRun {pyDir} inputFiles='{line}' outputFile='{nanoaodDir}nanoaod_{str(i*nCom+idx)}.root' &> {batchlogDir}nanoaod_{str(i*nCom+idx)}.log\n")
            shf.write(f"mv {batchlogDir}nanoaod_{str(i*nCom+idx)}.log {eoslogDir}\n")
    os.system("chmod 755 {}job_{}-{}.sh".format(shfilesDir, s, str(s+nCom-1)))
print("job.sh files created! Number of files: {}".format(len(slicing)))

###### Making submit.sub File ######
with open("submit.sub", 'w') as sub:
    sub.write("executable = $(filename)\n")
    sub.write("arguments  = $(ClusterId)$(ProcId)\n")
    sub.write("output     = {}$(ClusterId).$(ProcId).out\n".format(batchlogDir))
    sub.write("error      = {}$(ClusterId).$(ProcId).err\n".format(batchlogDir))
    sub.write("log        = {}$(ClusterId).log\n".format(batchlogDir))
    sub.write('+JobFlavour = "nextweek" \n')
    sub.write("\n")
    sub.write(f"queue filename matching files {shfilesDir}job*.sh")
print("submit.sub file created!")

###### Submitting Jobs ######
os.system("condor_submit submit.sub") # note that submit_jobs should be done in afs, unless it has -spool argument
print("Congratulations! Jobs are submitted.")
print("To check the status of the jobs, run the command condor_q.")
os.system("condor_q")