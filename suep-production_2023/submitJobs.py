"""
    This program creates and submits jobs for 2023 VBF MC generation.
    Command looks like: python3 submitJobs.py --nJobs=200 --nEvents=500 --toSave=['nanoaod'] --doSubmit --jobFlavour='tomorrow'
    Raymond Kil, 2024
"""

import os, time, stat
import random
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")

parser.add_option("--mass"       , dest="M"         , default="125"      , type=str           , help="Mediator mass in GeV. Default is 125")
parser.add_option("--decay"      , dest="decay"     , default="generic"  , type=str           , help="Decay mode of the dark photon (also determines the mass): leptonic, hadronic, generic_old (old, to dd) and generic (new, to 2pions).")
parser.add_option("--temperature", dest="T"         , default="2"        , type=str           , help="Temperature parameter. Default is 2")
parser.add_option("--nJobs"      , dest="nJobs"     , default=20         , type=int           , help="number of jobs to submit")
parser.add_option("--nEvents"    , dest="nEvents"   , default=1000       , type=int           , help="number of events per job")
parser.add_option("--toSave"     , dest="toSave"    , default=['nanoaod'], type=str           , help="data tiers to save, in format of list") # minor problem here... enter the argument for now.
parser.add_option("--doSubmit"   , dest="doSubmit"  , default=False      , action="store_true", help="If true, submit the jobs to condor")
parser.add_option("--jobFlavour" , dest="jobFlavour", default='tomorrow' , type=str           , help="job flavour to add in submit.sub file")
parser.add_option("--startpoint" , dest="startpoint", default=0          , type=int           , help="the starting number of the job submission.")
(options, args) = parser.parse_args()

tag        = f"M{options.M}{options.decay}T{options.T}"
nJobs      = options.nJobs
nEvents    = options.nEvents
toSave     = str(options.toSave).strip('[]').split(',')
doSubmit   = options.doSubmit
jobFlavour = options.jobFlavour
startpoint = options.startpoint

WORKDIR = f"/eos/user/j/jkil/vbftrigger/suep-production_2023/{tag}/"
if not os.path.exists(f'{WORKDIR}jobs')          : os.mkdir(f'{WORKDIR}jobs')
if not os.path.exists(f'{WORKDIR}jobs/batchlogs'): os.mkdir(f'{WORKDIR}jobs/batchlogs')
if not os.path.exists(f'{WORKDIR}jobs/exec')     : os.mkdir(f'{WORKDIR}jobs/exec')
if not os.path.exists(f'{WORKDIR}jobs/output')   : os.mkdir(f'{WORKDIR}jobs/output')
if not os.path.exists(f'{WORKDIR}jobs/proxy')    : os.mkdir(f'{WORKDIR}jobs/proxy')

for tier in toSave:
    if not os.path.exists(f'{WORKDIR}jobs/output/{tier}'): os.mkdir(f'{WORKDIR}jobs/output/{tier}')

if not os.path.isfile(f'{WORKDIR}jobs/proxy/x509up_u146772'): 
    os.system(f"voms-proxy-init -voms cms --rfc -valid 192:00 --out {WORKDIR}jobs/proxy/x509up_u146772")
elif time.time() - os.stat(f'{WORKDIR}jobs/proxy/x509up_u146772')[stat.ST_MTIME] > 3600*24:
    os.system(f"voms-proxy-init -voms cms --rfc -valid 192:00 --out {WORKDIR}jobs/proxy/x509up_u146772")

for j in range(startpoint, nJobs+startpoint):
    workdir = "/tmp/VBFSUEP_2023/"
    with open(f"{WORKDIR}jobs/exec/job_{j}.sh", 'w') as job:
        job.write("#!/bin/sh\n\n")
        job.write("echo '----- START -----'\n")
        #job.write(f"mkdir {workdir}\n")
        job.write(f"if [ ! -d {workdir} ]; then\n")
        job.write(f"    mkdir test_folder\n")
        job.write(f"    echo 'folder created.'\n")
        job.write(f"else\n")
        job.write(f"    echo 'folder already exists. Skipping this step...'\n")
        job.write(f"fi\n")
        job.write(f"cd {workdir}\n")
        job.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
        job.write(f"export X509_USER_PROXY={WORKDIR}jobs/proxy/x509up_u146772\n")
        username = os.getlogin()
        job.write(f"export HOME=/afs/cern.ch/user/{username[0]}/{username}\n\n")
        job.write(f"cd /eos/user/j/jkil/vbftrigger/suep-production_2023/CMSSW_13_0_14/src/\n")
        job.write("cmsenv\n")
        job.write("cd -\n")
        job.write("echo 'CMSSW_13_0_14 activated.'\n")
        job.write(f"\ncmsRun {WORKDIR}config_final/gensim.py outputFile=file:gensim_{j}.root maxEvents={nEvents} firstRun={j} seed={random.randint(0,1000000)} &> {WORKDIR}jobs/batchlogs/gensim_{j}.log\n")
        job.write("echo 'GENSIM created.'\n")
        job.write(f"\ncmsRun {WORKDIR}config_final/digihlt.py inputFiles=file:gensim_{j}_numEvent{nEvents}.root outputFile=file:digihlt_{j}.root &> {WORKDIR}jobs/batchlogs/digihlt_{j}.log\n")
        job.write("echo 'DIGIHLT created.'\n")
        if 'gensim' in toSave: job.write(f"cp gensim_{j}_numEvent{nEvents}.root {WORKDIR}jobs/output/gensim\n")
        job.write(f"rm gensim_{j}_numEvent{nEvents}.root\n")
        job.write(f"\ncmsRun {WORKDIR}config_final/aod.py inputFiles=file:digihlt_{j}.root outputFile=file:aod_{j}.root &> {WORKDIR}jobs/batchlogs/aod_{j}.log\n")
        job.write("echo 'AOD created.'\n")
        if 'digihlt' in toSave: job.write(f"cp digihlt_{j}.root {WORKDIR}jobs/output/digihlt\n")
        job.write(f"rm digihlt_{j}.root\n")
        job.write(f"\ncmsRun {WORKDIR}config_final/miniaod.py inputFiles=file:aod_{j}.root outputFile=file:miniaod_{j}.root &> {WORKDIR}jobs/batchlogs/miniaod_{j}.log\n")
        job.write("echo 'MINIAOD created.'\n")
        if 'aod' in toSave: job.write(f"cp aod_{j}.root {WORKDIR}jobs/output/aod\n")
        job.write(f"rm aod_{j}.root\n")
        job.write(f"\ncmsRun {WORKDIR}config_final/nanoaod.py inputFiles=file:miniaod_{j}.root outputFile=file:nanoaod_{j}.root &> {WORKDIR}jobs/batchlogs/nanoaod_{j}.log\n")
        job.write("echo 'NANOAOD created.'\n")
        if 'miniaod' in toSave: job.write(f"cp miniaod_{j}.root {WORKDIR}jobs/output/miniaod\n")
        job.write(f"rm miniaod_{j}.root\n")
        if 'nanoaod' in toSave: job.write(f"cp nanoaod_{j}.root {WORKDIR}jobs/output/nanoaod\n")
        job.write(f"rm nanoaod_{j}.root\n")

with open(f'{WORKDIR}jobs/submit.sub', 'w') as submit:
    submit.write('executable = $(filename)\n')
    submit.write('arguments  = $(ClusterId)$(ProcId)\n')
    submit.write('output     = $(ClusterId).$(ProcId).out\n')
    submit.write('error      = $(ClusterId).$(ProcId).err\n')
    submit.write('log        = $(ClusterId).log\n')
    submit.write(f'+JobFlavour = "{jobFlavour}" \n\n')
    submit.write(f'queue filename matching files {WORKDIR}jobs/exec/job*.sh')

if doSubmit: 
    os.system(f"condor_submit {WORKDIR}jobs/submit.sub -spool")
    print("Congratulations! Jobs are submitted.")
    os.system("condor_q")