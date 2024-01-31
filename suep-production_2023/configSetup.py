"""
    This program creates the config files for all data tiers.
    Make sure cmsenv is enabled.
    Raymond Kil, 2024
"""
import os
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")

parser.add_option("--datatier"         , dest="datatier"    , default="gensim" , type  ="string"    , help="which datatier to finalize the config file. Options: gensim, digihlt, aod, miniaod, nanoaod")
parser.add_option("--mass"       , "-M", dest="M"           , default="125"    , type  ="string"    , help="Mediator mass in GeV. Default is 125")
parser.add_option("--decay"            , dest="decay"       , default="generic", type  ="string"    , help="Decay mode of the dark photon (also determines the mass): leptonic, hadronic, generic_old (old, to dd) and generic (new, to 2pions).")
parser.add_option("--temperature", "-T", dest="T"           , default="2"      , type  ="string"    , help="Temperature parameter. Default is 2")
parser.add_option("--fragment"         , dest="fragment"    , default="VBF"    , type  ="string"    , help="file name of the fragment to use. Enter the string until _template.py")
(options, args) = parser.parse_args()

datatier     = options.datatier
mass         = options.M
decay        = options.decay
mPho         = '1' if decay=='generic' else '0.5' if decay=='leptonic' else '0.7' if decay=='hadronic' else 'invalid decay mode entered.'
temperature  = options.T
fragment     = options.fragment

print(f"---------- Start generating {datatier}.py ----------")

possibledecays = {'leptonic'   :"'999998:addChannel = 1 0.4 101 11 -11',\n'999998:addChannel = 1 0.4 101 13 -13',\n'999998:addChannel = 1 0.2 101 211 -211',\n",
                  'hadronic'   :"'999998:addChannel = 1 0.15 101 11 -11',\n'999998:addChannel = 1 0.15 101 13 -13',\n'999998:addChannel = 1 0.75 101 211 -211',\n",
                  'generic_old':"'999998:addChannel = 1 1 101 1 -1',\n",
                  'generic'    :"'999998:addChannel = 1 1 101 211 -211',\n"
}

if datatier=='gensim':
    # producing finalized fragment
    with open(f"fragments/{fragment}_template.py", 'r') as frag:
        frag_final = frag.read().replace('{[MHIGGS]}'     , mass)\
                                .replace('{[MPHO]}'       , mPho)\
                                .replace('{[DECAYS]}'     , possibledecays[decay])\
                                .replace('{[TEMPERATURE]}', temperature)\
                                .replace('process.generator = cms.EDFilter("Pythia8GeneratorFilter",','generator = cms.EDFilter("Pythia8GeneratorFilter",')
    with open(f"fragments/{fragment}_final.py", 'w') as frag:
        frag.write(frag_final)
    os.system("sh CMSSW_setup.sh")
    print("\nFragment made for gensim!\n")

# producing config template
print("Setting up folders...")
if not os.path.exists(f'config_final')   : os.mkdir(f'config_final')
if not os.path.exists(f'config_template'): os.mkdir(f'config_template')

config_args = {
    "gensim":{
        'FRAGMENT'        : f'PhysicsTools/SUEPNano/python/fragments/{fragment}_final.py',
        'PYTHON_FILENAME' : 'gensim_template.py',
        'EVENTCONTENT'    : 'RAWSIM',
        'CUSTOMISE'       : 'Configuration/DataProcessing/Utils.addMonitoring',
        'DATATIER'        : 'GEN-SIM',
        'FILEOUT'         : '{[FILEOUT]}',
        'CONDITIONS'      : '130X_mcRun3_2023_realistic_v14', #'130X_mcRun3_2023_realistic_postBPix_v2'
        'BEAMSPOT'        : 'Realistic25ns13p6TeVEarly2023Collision',
        #'CUSTOMISE_COMMANDS' : 'process.source.numberEventsInLuminosityBlock=cms.untracked.uint32(510400)'
        'STEP'            : 'GEN,SIM',
        'GEOMETRY'        : 'DB:Extended',
        'ERA'             : 'Run3_2023',
        'NO_EXEC'         : '',
        'MC'              : '',
        'N'               : '-13596'
        },
    "digihlt":{
        'CONFIG_STEP'     : 'step1',
        'PYTHON_FILENAME' : 'digihlt_template.py',
        'EVENTCONTENT'    : 'PREMIXRAW',
        'CUSTOMISE'       : 'Configuration/DataProcessing/Utils.addMonitoring',
        'DATATIER'        : 'GEN-SIM-RAW',
        'FILEIN'          : '{[FILEIN]}',
        'FILEOUT'         : '{[FILEOUT]}',
        'PILEUP_INPUT'    : 'dbs:/Neutrino_E-10_gun/Run3Summer21PrePremix-Summer23_130X_mcRun3_2023_realistic_v13-v1/PREMIX',
        'CONDITIONS'      : '130X_mcRun3_2023_realistic_v14',
        'STEP'            : 'DIGI,DATAMIX,L1,DIGI2RAW,HLT:2023v12',
        'PROCMODIFIERS'   : 'premix_stage2,siPixelQualityRawToDigi',
        'NTHREADS'        : '1',
        'GEOMETRY'        : 'DB:Extended',
        'DATAMIX'         : 'PreMix',
        'ERA'             : 'Run3_2023',
        'NO_EXEC'         : '',
        'MC'              : '',
        'N'               : '-13596'
    },
    "aod":{
        'CONFIG_STEP'     : 'step2',
        'PYTHON_FILENAME' : 'aod_template.py',
        'EVENTCONTENT'    : 'AODSIM',
        'DATATIER'        : 'AODSIM',
        'FILEIN'          : '{[FILEIN]}',
        'FILEOUT'         : '{[FILEOUT]}',
        'CONDITIONS'      : '130X_mcRun3_2023_realistic_v14',
        'STEP'            : 'RAW2DIGI,L1Reco,RECO,RECOSIM',
        'NTHREADS'        : '1',
        'GEOMETRY'        : 'DB:Extended',
        'ERA'             : 'Run3_2023',
        'NO_EXEC'         : '',
        'MC'              : '',
        'N'               : '-13596'
    },
    "miniaod":{
        'CONFIG_STEP'     : 'step1',
        'PYTHON_FILENAME' : 'miniaod_template.py',
        'EVENTCONTENT'    : 'MINIAODSIM',
        'DATATIER'        : 'MINIAODSIM',
        'FILEIN'          : '{[FILEIN]}',
        'FILEOUT'         : '{[FILEOUT]}',
        'CONDITIONS'      : '130X_mcRun3_2023_realistic_v14',
        'STEP'            : 'PAT',
        'NTHREADS'        : '1',
        'GEOMETRY'        : 'DB:Extended',
        'ERA'             : 'Run3_2023',
        'NO_EXEC'         : '',
        'MC'              : '',
        'N'               : '-13596'
    },
    "nanoaod":{
        'CONFIG_STEP'     : 'step1',
        'PYTHON_FILENAME' : 'nanoaod_template.py',
        'EVENTCONTENT'    : 'NANOAODSIM',
        'DATATIER'        : 'NANOAODSIM',
        'FILEIN'          : '{[FILEIN]}',
        'FILEOUT'         : '{[FILEOUT]}',
        'CONDITIONS'      : '130X_mcRun3_2023_realistic_v14',
        'STEP'            : 'NANO',
        'NTHREADS'        : '1',
        'SCENARIO'        : 'pp',
        'ERA'             : 'Run3_2023',
        'NO_EXEC'         : '',
        'MC'              : '',
        'N'               : '-13596'
    }
}

options_string = f"from Configuration.Eras.Era_{config_args[datatier]['ERA']}_cff import {config_args[datatier]['ERA']}\
    \nimport FWCore.ParameterSet.VarParsing as VarParsing\
    \n\
    \n# setup 'analysis' options\
    \noptions = VarParsing.VarParsing ('analysis')\
    \n\
    \n# setup any defaults you want\
    \noptions.outputFile = 'output.root'\
    \noptions.inputFiles = ['input.root']\
    \noptions.maxEvents = -1 # -1 means all events\
    \n\
    \noptions.register('seed',123456, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int)\
    \noptions.seed = 123456\
    \noptions.register( 'firstRun',\
    \n                1,  #default value\
    \n                VarParsing.VarParsing.multiplicity.singleton,\
    \n                VarParsing.VarParsing.varType.int,\
    \n                'the first run'\
    \n                )\
    \n\
    \noptions.parseArguments()\
"

# Generating config_template
print("\nStart generating config_template\n")
if datatier=='digihlt': os.system(f"voms-proxy-init -voms cms --rfc -valid 192:00")

if   datatier=='gensim' : os.system(f"cmsDriver.py {config_args['gensim']['FRAGMENT']} --python_filename {config_args['gensim']['PYTHON_FILENAME']} --eventcontent {config_args['gensim']['EVENTCONTENT']} --customise {config_args['gensim']['CUSTOMISE']} --datatier {config_args['gensim']['DATATIER']} --fileout {config_args['gensim']['FILEOUT']} --conditions {config_args['gensim']['CONDITIONS']} --beamspot {config_args['gensim']['BEAMSPOT']} --step {config_args['gensim']['STEP']} --geometry {config_args['gensim']['GEOMETRY']} --era {config_args['gensim']['ERA']} --no_exec --mc -n {config_args['gensim']['N']}")
elif datatier=='digihlt': os.system(f"cmsDriver.py {config_args['digihlt']['CONFIG_STEP']} --python_filename {config_args['digihlt']['PYTHON_FILENAME']} --eventcontent {config_args['digihlt']['EVENTCONTENT']} --customise {config_args['digihlt']['CUSTOMISE']} --datatier {config_args['digihlt']['DATATIER']} --fileout {config_args['digihlt']['FILEOUT']} --pileup_input {config_args['digihlt']['PILEUP_INPUT']} --conditions {config_args['digihlt']['CONDITIONS']} --step {config_args['digihlt']['STEP']} --procModifiers {config_args['digihlt']['PROCMODIFIERS']} --nThreads {config_args['digihlt']['NTHREADS']} --geometry {config_args['digihlt']['GEOMETRY']} --filein {config_args['digihlt']['FILEIN']} --datamix {config_args['digihlt']['DATAMIX']} --era {config_args['digihlt']['ERA']} --no_exec --mc -n {config_args['digihlt']['N']}")
elif datatier=='aod'    : os.system(f"cmsDriver.py {config_args['aod']['CONFIG_STEP']} --python_filename {config_args['aod']['PYTHON_FILENAME']} --eventcontent {config_args['aod']['EVENTCONTENT']} --datatier {config_args['aod']['DATATIER']} --filein {config_args['aod']['FILEIN']} --fileout {config_args['aod']['FILEOUT']} --conditions {config_args['aod']['CONDITIONS']} --step {config_args['aod']['STEP']} --nThreads {config_args['aod']['NTHREADS']} --geometry {config_args['aod']['GEOMETRY']} --era {config_args['aod']['ERA']} --no_exec --mc -n {config_args['aod']['N']}")
elif datatier=='miniaod': os.system(f"cmsDriver.py {config_args['miniaod']['CONFIG_STEP']} --python_filename {config_args['miniaod']['PYTHON_FILENAME']} --eventcontent {config_args['miniaod']['EVENTCONTENT']} --datatier {config_args['miniaod']['DATATIER']} --filein {config_args['miniaod']['FILEIN']} --fileout {config_args['miniaod']['FILEOUT']} --conditions {config_args['miniaod']['CONDITIONS']} --step {config_args['miniaod']['STEP']} --nThreads {config_args['miniaod']['NTHREADS']} --geometry {config_args['miniaod']['GEOMETRY']} --era {config_args['miniaod']['ERA']} --no_exec --mc -n {config_args['miniaod']['N']}")
elif datatier=='nanoaod': os.system(f"cmsDriver.py {config_args['nanoaod']['CONFIG_STEP']} --python_filename {config_args['nanoaod']['PYTHON_FILENAME']} --eventcontent {config_args['nanoaod']['EVENTCONTENT']} --datatier {config_args['nanoaod']['DATATIER']} --filein {config_args['nanoaod']['FILEIN']} --fileout {config_args['nanoaod']['FILEOUT']} --conditions {config_args['miniaod']['CONDITIONS']} --step {config_args['nanoaod']['STEP']} --nThreads {config_args['nanoaod']['NTHREADS']} --scenario {config_args['nanoaod']['SCENARIO']} --era {config_args['nanoaod']['ERA']} --no_exec --mc -n {config_args['nanoaod']['N']}")
os.system(f'mv {datatier}_template.py config_template')
print(f"{datatier}_template.py succefssfully made: ./config_template/{datatier}_template.py")

# Generating config_final
if datatier=='gensim':
    with open(f"config_template/{datatier}_template.py", 'r') as template:
        with open(f"{datatier}.py",'w') as final:
            final.write(
                template.read().replace(f"from Configuration.Eras.Era_{config_args['gensim']['ERA']}_cff import {config_args['gensim']['ERA']}", options_string)\
                               .replace('-13596', 'options.maxEvents')\
                               .replace("    fileName = cms.untracked.string('{[FILEOUT]}'),", "    fileName = cms.untracked.string(options.outputFile),")
            )
    os.remove(f"fragments/{fragment}_final.py")
else:
    with open(f"config_template/{datatier}_template.py", 'r') as template:
        with open(f"{datatier}.py",'w') as final:
            final.write(
                template.read().replace(f"from Configuration.Eras.Era_{config_args[datatier]['ERA']}_cff import {config_args[datatier]['ERA']}", options_string)\
                               .replace("-13596", "options.maxEvents")\
                               .replace("'{[FILEIN]}'" , "options.inputFiles")\
                               .replace("'{[FILEOUT]}'", "options.outputFile") 
            )
os.system(f"mv {datatier}.py config_final")
print(f"{datatier}.py succefssfully made: ./config_final/{datatier}.py\n")

# move config_template, config_final, and jobs into tag
tag = f"M{mass}{decay}T{temperature}"
if not os.path.exists(tag): os.mkdir(tag)
tem_cond = len([f for f in [t+'_template.py' for t in config_args.keys()] if f in os.listdir('config_template')])==5
fin_cond = len([f for f in [t+'.py' for t in config_args.keys()] if f in os.listdir('config_final')])==5
if tem_cond and fin_cond:
    os.system(f'mv config_template {tag}')
    os.system(f'mv config_final {tag}')