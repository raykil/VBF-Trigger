import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
	maxEventsToPrint = cms.untracked.int32(1),
	pythiaPylistVerbosity = cms.untracked.int32(1),
	filterEfficiency = cms.untracked.double(1),
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	comEnergy = cms.double(13600.0),
	crossSection = cms.untracked.double(1),
	PythiaParameters = cms.PSet(
            pythia8CommonSettingsBlock,
            pythia8CP5SettingsBlock,
            pythia8PSweightsSettingsBlock,
            processParameters = cms.vstring(
              'Check:event = off', #Might be needed, but it seems to run without
              'HiggsSM:all = off', # Other Higgs channels off
              'HiggsSM:ff2Hff(t:ZZ) = on', # ZZ VBF production
              'HiggsSM:ff2Hff(t:WW) = on', # WW VBF production
              '25:m0 =  {[MHIGGS]}', # Mediator is SM Higgs. Current for ggF: 125,200,300,400,750,1000
              '25:onMode = off',      # turn off all H decays
              '25:onIfMatch = 4 -4', ## turn on H -> tau tau
            ),
            parameterSets = cms.vstring('pythia8CommonSettings',
                                        'pythia8CP5Settings',
                                        'pythia8PSweightsSettings',
                                        'processParameters',
           )
	),
)


