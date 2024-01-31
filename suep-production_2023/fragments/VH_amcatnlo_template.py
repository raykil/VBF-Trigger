import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *

process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/vh012j_5f_NLO/vh012j_5f_NLO_FXFX_M125_VToAll_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'),
    nEvents = cms.untracked.uint32({[MAXEVENTS]}),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
	maxEventsToPrint = cms.untracked.int32(1),
	pythiaPylistVerbosity = cms.untracked.int32(1),
	filterEfficiency = cms.untracked.double(1),
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	comEnergy = cms.double(13000.0),
	crossSection = cms.untracked.double(1),
	PythiaParameters = cms.PSet(
            pythia8CommonSettingsBlock,
            pythia8CP5SettingsBlock,
            pythia8PSweightsSettingsBlock,
            pythia8aMCatNLOSettingsBlock,
            processParameters = cms.vstring(
              'Check:event = off', #Might be needed, but it seems to run without
              'JetMatching:setMad = off',
              'JetMatching:scheme = 1',
              'JetMatching:merge = on',
              'JetMatching:jetAlgorithm = 2',
              'JetMatching:etaJetMax = 999.',
              'JetMatching:coneRadius = 1.',
              'JetMatching:slowJetPower = 1',
              'JetMatching:qCut = 18.',
              'JetMatching:doFxFx = on',
              'JetMatching:qCutME = 10.',
              'JetMatching:nQmatch = 5',
              'JetMatching:nJetMax = 2',
              'SLHA:useDecayTable = off',
              'Check:event = off', #Might be needed, it complains when we undo the Higgs decays
              'HiggsSM:all = off', # Other Higgs channels off
              '25:m0 = 125', # Mediator is SM Higgs. Current for ggF: 125,200,300,400,750,1000
              '999999:all = GeneralResonance void 0 0 0 2 0.001 0.0 0.0 0.0', # The dark meson definition: name, antiname, spin=2s+1 (0=undef), charge*3, color (0=single, 1=triplet, 2=octet), m0, width, mMin, mMax, tau
              '999998:all = GeneralResonance void 1 0 0 {[MPHO]} 0.001 0.0 0.0 0.0', # A dark boson which is a color triplet
              '999999:addChannel = 1 1.0 101 999998 999998 ', # First dark particle decays to a pair of the second
              {[DECAYS]}
            ),
            parameterSets = cms.vstring('pythia8CommonSettings',
                                        'pythia8CP5Settings',
                                        'pythia8aMCatNLOSettings',
                                        'pythia8PSweightsSettings',
                                        'processParameters',
           )
	),
        UserCustomization = cms.VPSet(
           cms.PSet(
             pluginName = cms.string("SuepDecay"),
             idDark = cms.int32(999999), # pdgId of the dark meson
             idMediator = cms.int32(25), # pdgId of the mediator
             temperature = cms.double({[TEMPERATURE]}) # Temperature of the thermal distribution
           )
        ),
)
