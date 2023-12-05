#!/usr/bin/env python
import os, re, stat
import commands
import math, time
import sys     
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
import ROOT # This is needed to check if files exist
from numpy import random

print("") 
print('START')
print("")
########   YOU ONLY NEED TO FILL THE AREA BELOW   #########
########   customization  area #########
# Signal stuff

parser.add_option("--channel"          , dest="channel"     , default="ggHBSM"   , type="string"      , help="Production mode: ggH (wide width mediator), ggHBSM (narrow width mediator, preferred), VBF, VH, ttH. Default is ggHBSM")
parser.add_option("--generator"        , dest="generator"   , default="pythia"   , type="string"      , help="ME generator: pythia or amcatnlo (later only available for mH=125). Default is pythia")
parser.add_option("--decay"            , dest="decay"       , default="generic"  , type="string"      ,  help="Decay mode of the dark photon (also determines the mass): leptonic, hadronic, generic_old (old, to dd) and generic (new, to 2pions). Default is generic")
parser.add_option("--temperature", "-T", dest="T"           , default="2"        , type="string"      , help="Temperature parameter. Default is 2")
parser.add_option("--mass"       , "-M", dest="M"           , default="125"      , type="string"      , help="Mediator mass in GeV. Default is 125")
parser.add_option("--queue"            , dest="queue"       , default="tomorrow" , type="string"      , help="Submission queue to use in condor. Default is tomorrow")
parser.add_option("--batch"            , dest="batch"       , default="slurm"    , type="string"      , help="Batch system to use (condor/slurm). Default is slurm")
parser.add_option("--jobs"       , "-j", dest="jobs"        , default=20         , type=int           , help="How many jobs to run. Default is 20")
parser.add_option("--djobs"            , dest="djobs"       , default=0          , type=int           , help="Create/check jobs starting from this job number. A easy way to generate extensions to previous samples that ensure statistical independence. Default is 0")
parser.add_option("--events"     , "-e", dest="events"      , default=1000       , type=int           , help="Events run per job before filter. Note: actual events produced are events*filter_efficiency. Default is 1000")
parser.add_option("--year"       , "-y", dest="year"        , default="UL18"     , type="string"      , help="Which year to produce (UL18, UL17, UL16, UL16APV). Default is UL18")
parser.add_option("--tag"        , "-t", dest="tag"         , default=""         , type="string"      , help="Extra tag to add to the submission folder and files (i.e. for extensions). Default is """)
parser.add_option("--mDark"            , dest="mdark"       , default="2"        , type="string"      , help="Mass of the dark meson. Default is 2")
parser.add_option("--htcut"            , dest="htcut"       , default="-1"       , type="string"      , help="Gen level HT cut (only available for ggH channel). -1 means no filter is applied which is different from 0.0. Default is -1, no cut")
parser.add_option("--outputdir"        , dest="outputdir"   , default="/."       , type="string"      , help="Where to put the samples. Default is /work/submit/cericeci/SUEP/private_samples which you might not have permissions to write to.")
parser.add_option("--pretend"          , dest="pretend"     , default=False      , action="store_true", help="If activated, just create submission files but don't submit anything")
parser.add_option("--toSave"           , dest="toSave"      , default=["NANOAOD"], action="append"    , help="Data tiers to save (NANOAOD, MINIAOD, AOD, HLT, SIM-DIGI, GEN). Can be given more than once. Default is just NANOAOD.")
parser.add_option("--fullgen"          , dest="fullgen"     , default=False      , action="store_true", help="If activated, will save full gen information for the signal (useful for truth level track matching)")
parser.add_option("--fullfragment"     , dest="fullfragment", default=None       , type="string"      , help="If activated, will just use the input file for the overall fragment instead of creating it")
(options, args) = parser.parse_args()

channel      = options.channel if float(options.htcut) < 0 else options.channel + "HTCut"
generator    = options.generator
decayshort   = options.decay
T            = options.T
M            = options.M
queue        = options.queue
NumberOfJobs = options.jobs
EventsPerJob = options.events
year         = options.year
tag          = options.tag
mdark        = options.mdark
ht           = options.htcut
dj = options.djobs
batch        = options.batch
doSubmit = not(options.pretend)
workdir = "/".join(os.getcwd().split("/")[:-1])

# To account for cases in which not all events pass gen filters/matching when doing strict cheking of existing files
matchEff = 0.1 if ((generator!="pythia") or ("HT" in channel)) else 1

gentemplate = "genpythia_template.py" if not "HT" in channel else "genpythiawithht_template.py" 
fragment    = "../fragments/%s_template.py"%(channel) if not(options.fullfragment) else "../fragments/%s"%(options.fullfragment)
if generator == "amcatnlo": # Kind of experimental, doing SUEP decay from gridpacks, NLO accuracy is NOT ensured as SUEP shower might breaking the matching
  if M != "125":
    raise RuntimeError("No gridpack for that, sorry")
  if channel == "VBF" :
    gentemplate = "gen_template.py"
    fragment    = "../fragments/VBF_amcatnlo_template.py"
  elif channel == "VH":
    gentemplate = "gen_template.py" 
    fragment    = "../fragments/VH_amcatnlo_template.py"
  else: 
    raise RuntimeError("Wrong generator-channel configuration")
if "Run3" in year: # Only pythia implemented for Run 3 yet
  gentemplate = "gensimpythia_template.py" 

OutputDir = "%s/%s/%s%s_%s_M%s_MD%s_T%s_HT%s_%s/"%(options.outputdir, year,channel, generator, decayshort, M, mdark, T, ht, tag) if not options.fullfragment else "%s/%s/%s"%(options.outputdir, options.year, options.fullfragment.replace(".py",""))
if not os.path.isdir(options.outputdir): os.system("mkdir %s"%options.outputdir)
if not os.path.isdir("%s/%s"%(options.outputdir, year)): os.system("mkdir %s/%s"%(options.outputdir, year))

tag       = "suep_%s_T%s_MD%s_%s_%s%s_%s_%s"%(M,T,mdark,decayshort,channel,generator,ht,year) if not options.fullfragment else "suep_%s_%s"%(options.fullfragment.replace(".py",""), options.year)
toSave = options.toSave
print(toSave)
releases = {"UL18":{"GEN":"CMSSW_10_6_30_patch1",
                    "SIM-DIGI": "CMSSW_10_6_30_patch1",
                    "HLT": "CMSSW_10_2_16_UL",
                    "AOD": "CMSSW_10_6_30_patch1",
                    "MINIAOD": "CMSSW_10_6_30_patch1",
                    "NANOAOD": "CMSSW_10_6_30_patch1"
                   },
            "UL17":{"GEN": "CMSSW_10_6_30_patch1",
                    "SIM-DIGI": "CMSSW_10_6_30_patch1",
                    "HLT": "CMSSW_9_4_14_UL_patch1",
                    "AOD": "CMSSW_10_6_30_patch1",
                    "MINIAOD": "CMSSW_10_6_30_patch1",
                    "NANOAOD": "CMSSW_10_6_30_patch1"
                   },
            "UL16APV":{"GEN":"CMSSW_10_6_30_patch1",
                    "SIM-DIGI": "CMSSW_10_6_30_patch1",
                    "HLT": "CMSSW_8_0_33_UL",
                    "AOD": "CMSSW_10_6_30_patch1",
                    "MINIAOD": "CMSSW_10_6_30_patch1",
                    "NANOAOD": "CMSSW_10_6_30_patch1"
                   },
            "UL16":{"GEN":"CMSSW_10_6_30_patch1",
                    "SIM-DIGI": "CMSSW_10_6_30_patch1",
                    "HLT": "CMSSW_8_0_33_UL",
                    "AOD": "CMSSW_10_6_30_patch1",
                    "MINIAOD": "CMSSW_10_6_30_patch1",
                    "NANOAOD": "CMSSW_10_6_30_patch1"
                   },
            "Run3Summer22EE":{
                    "GEN-SIM" : "CMSSW_12_4_11_patch3",
                    "DIGI-HLT": "CMSSW_12_4_11_patch3",
                    "AOD"     : "CMSSW_12_4_11_patch3",
                    "MINIAOD" : "CMSSW_12_4_11_patch3",
                    "NANOAOD" : "CMSSW_12_6_0_patch1"
            },
            "Run3Summer22":{
                    "GEN-SIM" : "CMSSW_12_4_11_patch3",
                    "DIGI-HLT": "CMSSW_12_4_11_patch3",
                    "AOD"     : "CMSSW_12_4_11_patch3",
                    "MINIAOD" : "CMSSW_12_4_11_patch3",
                    "NANOAOD" : "CMSSW_12_6_0_patch1"
            },
}

steps = releases[year].keys() 
########   customization end   #########


possibledecays = {'leptonic':   "'999998:addChannel = 1 0.4 101 11 -11',\n'999998:addChannel = 1 0.4 101 13 -13',\n'999998:addChannel = 1 0.2 101 211 -211',\n",
                  'hadronic':   "'999998:addChannel = 1 0.15 101 11 -11',\n'999998:addChannel = 1 0.15 101 13 -13',\n'999998:addChannel = 1 0.75 101 211 -211',\n",
                  'generic_old'    :"'999998:addChannel = 1 1 101 1 -1',\n", # This used to be our "old" generic definition
                  'generic':"'999998:addChannel = 1 1 101 211 -211',\n"
}

mPho = 1
if decayshort == "leptonic": mPho = 0.5
if decayshort == "hadronic": mPho = 0.7

FullOutputDir = "%s/"%(OutputDir)
print("")
print('do not worry about folder creation:')
os.system("rm -rf %s/tmp"%tag)
os.system("rm -rf %s/exec"%tag)
os.system("rm -rf %s/batchlogs"%tag)
os.system("mkdir %s"%tag)
os.system("mkdir %s/tmp"%tag)
os.system("mkdir %s/exec"%tag)
os.system("mkdir %s/batchlogs"%tag)
os.system("mkdir %s" %FullOutputDir)
print("mkdir %s" %FullOutputDir)
for step in steps:
  os.system("mkdir %s/%s/" %(FullOutputDir, step))

os.system("cp %s/*py %s"%(year + ("_withgeninfo" if options.fullgen else ""), tag))

genTemplate = open("%s/%s"%(tag, gentemplate), "r")
fragment    = open(fragment)
genFinal    = open("%s/gen_final.py"%tag,"w")

if mPho > float(mdark)/2.: mPho = float(mdark)/2.*0.99 ## Just so decays are enabled
text = genTemplate.read().replace("{[FRAGMENT]}", fragment.read().replace("{[DECAYS]}",possibledecays[decayshort]).replace("{[DECAYSHORT]}", "'%s'"%decayshort).replace("{[TEMPERATURE]}",T).replace("{[MAXEVENTS]}",str(EventsPerJob)).replace("{[MHIGGS]}",M).replace("{[MPHO]}", str(mPho)).replace("{[MDARK]}",mdark)).replace("{[HTCUT]}", ht)

genFinal.write(text)

proxyfile = "%s/test/proxy/proxy"%workdir
if not(os.path.isfile(proxyfile)):
  os.system("voms-proxy-init -voms cms --rfc -valid 192:00 --out %s"%proxyfile)
elif time.time() - os.stat(proxyfile)[stat.ST_MTIME] > 3600*24: # i.e. recreate proxy if it is more than one day old
  os.system("voms-proxy-init -voms cms --rfc -valid 192:00 --out %s"%proxyfile)

iJob = 0 + dj
##### loop for creating and sending jobs #####
for x in range(1001+dj, int(NumberOfJobs+1000)+1+dj):
    ##### creates directory and file list for job #######
    ####### Quickly checks if nano already available and not empty:
    redo = True
    print("Looking for %s"%("%s/nanoaod_%i.root"%(FullOutputDir+"/NANOAOD/",x)))
    if os.path.isfile("%s/nanoaod_%i.root"%(FullOutputDir+"/NANOAOD/",x)):
        rt = ROOT.TFile("%s/nanoaod_%i.root"%(FullOutputDir+"/NANOAOD/",x), "READ")
        tf = rt.Get("Events")
        redo = False
        if type(tf) != type(ROOT.TTree()):
            print("Something went wrong with %s, redoing..."%("%s/nanoaod_%i.root"%(FullOutputDir+"/NANOAOD/",x)))
            redo = True
        elif (tf.GetEntries() != EventsPerJob) and matchEff == 1: #With matching it might not be equal
            print("Tree %s has less than the requested events, redoing..."%("%s/nanoaod_%i.root"%(FullOutputDir+"/NANOAOD/",x)))
            redo = True

    if redo:     
      iJob += 1
      ####### creates jobs #######
      with open('%s/exec/job_'%tag+str(iJob)+'.sh', 'w') as fout:
        fout.write("#!/bin/sh\n")
        fout.write("echo\n")
        fout.write("echo\n")
        fout.write("echo 'START---------------'\n")
        fout.write("mkdir /tmp/_%s%i/\n"%(tag,iJob))
        fout.write("cd /tmp/_%s%i/\n"%(tag,iJob))
        fout.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
        fout.write("export X509_USER_PROXY=%s\n"%proxyfile)
        username = os.getlogin()
        fout.write("export HOME=/afs/cern.ch/user/%s/%s\n"%(username[0], username))
        fout.write("echo 'WORKDIR ' ${PWD}\n")
        if "Run3" in year:

          fout.write("cd %s/%s/src/\n"%(workdir,releases[year]["GEN-SIM"]))
          fout.write("cmsenv\n")
          fout.write("cd -\n")
          fout.write("cmsRun %s/test/%s/gen_final.py outputFile=file:gensim_%i.root maxEvents=%i firstRun=%i seed=%i &> %s/test/%s/batchlogs/gensim_%i.log \n"%(workdir, tag,x, EventsPerJob, x, random.randint(1000000), workdir, tag, x))
          if "GEN-SIM" in toSave: fout.write("cp gensim_%i_numEvent%i.root %s\n"%(x,EventsPerJob,FullOutputDir+"/GEN-SIM/"))
          fout.write("cd %s/%s/src/\n"%(workdir,releases[year]["DIGI-HLT"]))
          fout.write("cmsenv\n")
          fout.write("cd -\n")

          fout.write("cmsRun %s/test/%s/digihlt.py inputFiles=file:gensim_%i_numEvent%i.root outputFile=file:digihlt_%i.root &> %s/test/%s/batchlogs/digihlt_%i.log\n"%(workdir, tag,x,EventsPerJob,x, workdir, tag, x))

          fout.write("rm gensim_%i_numEvent%i.root\n"%(x,EventsPerJob))
          if "DIGI-HLT" in toSave: fout.write("cp digihlt_%i.root %s\n"%(x,FullOutputDir+"/DIGI-HLT/"))

          fout.write("cd %s/%s/src/\n"%(workdir,releases[year]["AOD"]))
          fout.write("cmsenv\n")
          fout.write("cd -\n")

          fout.write("cmsRun %s/test/%s/aod.py inputFiles=file:digihlt_%i.root outputFile=file:aod_%i.root &> %s/test/%s/batchlogs/aod_%i.log \n"%(workdir, tag,x,x, workdir, tag,x))
          fout.write("rm digihlt_%i.root\n"%x)

          fout.write("cd %s/%s/src/\n"%(workdir,releases[year]["MINIAOD"]))
          fout.write("cmsenv\n")
          fout.write("cd -\n")
          if "AOD" in toSave: fout.write("cp aod_%i.root %s\n"%(x,FullOutputDir+"/AOD/"))

          fout.write("cmsRun %s/test/%s/miniaod.py inputFiles=file:aod_%i.root outputFile=file:miniaod_%i.root &> %s/test/%s/batchlogs/mini_%i.log\n"%(workdir, tag,x,x, workdir, tag, x))
          fout.write("rm aod_%i.root\n"%x)
          if "MINIAOD" in toSave: fout.write("cp miniaod_%i.root %s\n"%(x,FullOutputDir+"/MINIAOD/"))

          fout.write("cd %s/%s/src/\n"%(workdir,releases[year]["NANOAOD"]))
          fout.write("cmsenv\n")
          fout.write("cd -\n")

          fout.write("cmsRun %s/test/%s/nanoaod.py inputFiles=file:miniaod_%i.root outputFile=file:nanoaod_%i.root &> %s/test/%s/batchlogs/nano_%i.log\n"%(workdir, tag,x,x, workdir, tag,x))
          fout.write("rm miniaod_%i.root\n"%x)
          if "NANOAOD" in toSave: fout.write("cp nanoaod_%i.root %s\n"%(x,FullOutputDir+"/NANOAOD/"))
          fout.write("rm nanoaod_%i.root\n"%x)


        elif "UL" in year:
          fout.write("cd %s/%s/src/\n"%(workdir,releases[year]["GEN"]))
          fout.write("cmsenv\n")
          fout.write("cd -\n")
          fout.write("cmsRun %s/test/%s/gen_final.py outputFile=file:gen_%i.root maxEvents=%i firstRun=%i seed=%i &> %s/test/%s/batchlogs/gen_%i.log \n"%(workdir, tag,x, EventsPerJob, x, random.randint(1000000), workdir, tag, x))
          if "GEN" in toSave: fout.write("cp gen_%i_numEvent%i.root %s\n"%(x,EventsPerJob,FullOutputDir+"/GEN/"))

          fout.write("cmsRun %s/test/%s/sim-digi_pythia.py inputFiles=file:gen_%i_numEvent%i.root outputFile=file:sim_digi_%i.root &> %s/test/%s/batchlogs/simdigi_%i.log\n"%(workdir, tag,x,EventsPerJob,x, workdir, tag, x)) 

          fout.write("rm gen_%i_numEvent%i.root\n"%(x,EventsPerJob))
          fout.write("cd %s/%s/src/\n"%(workdir,releases[year]["HLT"]))
          fout.write("cmsenv\n")
          fout.write("cd -\n")
          if "SIM-DIGI" in toSave: fout.write("cp sim_digi_%i.root %s\n"%(x,FullOutputDir+"/SIM-DIGI/"))

          fout.write("cmsRun %s/test/%s/hlt_pythia.py inputFiles=file:sim_digi_%i.root outputFile=file:hlt_%i.root &> %s/test/%s/batchlogs/hlt_%i.log\n"%(workdir, tag,x,x, workdir,tag,x))
          fout.write("rm sim_digi_%i.root\n"%x)

          fout.write("cd %s/%s/src/\n"%(workdir,releases[year]["AOD"]))
          fout.write("cmsenv\n")
          fout.write("cd -\n")

          fout.write("cmsRun %s/test/%s/aod_pythia.py inputFiles=file:hlt_%i.root outputFile=file:aod_%i.root &> %s/test/%s/batchlogs/aod_%i.log \n"%(workdir, tag,x,x, workdir, tag,x))
          fout.write("rm hlt_%i.root\n"%x)


          fout.write("cd %s/%s/src/\n"%(workdir,releases[year]["MINIAOD"]))
          fout.write("cmsenv\n")
          fout.write("cd -\n")
          if "AOD" in toSave: fout.write("cp aod_%i.root %s\n"%(x,FullOutputDir+"/AOD/"))

          fout.write("cmsRun %s/test/%s/miniaod_pythia.py inputFiles=file:aod_%i.root outputFile=file:miniaod_%i.root &> %s/test/%s/batchlogs/mini_%i.log\n"%(workdir, tag,x,x, workdir, tag, x))
          fout.write("rm aod_%i.root\n"%x)
          if "MINIAOD" in toSave: fout.write("cp miniaod_%i.root %s\n"%(x,FullOutputDir+"/MINIAOD/"))

          fout.write("cd %s/%s/src/\n"%(workdir,releases[year]["NANOAOD"]))
          fout.write("cmsenv\n")
          fout.write("cd -\n")

          fout.write("cmsRun %s/test/%s/nanoaod_pythia.py inputFiles=file:miniaod_%i.root outputFile=file:nanoaod_%i.root &> %s/test/%s/batchlogs/nano_%i.log\n"%(workdir, tag,x,x, workdir, tag,x))
          fout.write("rm miniaod_%i.root\n"%x)
          if "NANOAOD" in toSave: fout.write("cp nanoaod_%i.root %s\n"%(x,FullOutputDir+"/NANOAOD/"))
          fout.write("rm nanoaod_%i.root\n"%x)

          fout.write("rm -rf /tmp/_%s%i/\n"%(tag,iJob))
          fout.write("echo 'STOP---------------'\n")
          fout.write("echo\n")
          fout.write("echo\n")
      os.system("chmod 755 %s/exec/job_"%tag+str(iJob)+".sh")
   
###### create submit.sub file ####
if iJob == 0:
    print("No new jobs to submit, closing in...")
    exit()
else:
    print("Will submit %s new jobs"%iJob)
#os.mkdir("%s/batchlogs"%tag)
if batch == "condor":
  with open('submit.sub', 'w') as fout:
    fout.write("executable              = $(filename)\n")
    fout.write("arguments               = $(ClusterId)$(ProcId)\n")
    fout.write("output                  = %s/batchlogs/$(ClusterId).$(ProcId).out\n"%tag)
    fout.write("error                   = %s/batchlogs/$(ClusterId).$(ProcId).err\n"%tag)
    fout.write("log                     = %s/batchlogs/$(ClusterId).log\n"%tag)
    fout.write('+JobFlavour = "%s"\n' %(queue))
    fout.write("\n")
    fout.write("queue filename matching (%s/exec/job_*sh)\n"%tag)

  if doSubmit:    
    ###### sends bjobs ######
    os.system("echo submit.sub")
    os.system("condor_submit -spool submit.sub")
   
    print("")
    print("your jobs:")
    os.system("condor_q")
    print("")
    print('END')

elif batch == "slurm":
  iJob = 0 + dj
  if doSubmit:
    for x in range(1001+dj, int(NumberOfJobs+1000)+1+dj):
      iJob += 1
      os.system("sbatch  %s/exec/job_"%tag+str(iJob)+".sh")

print("")
