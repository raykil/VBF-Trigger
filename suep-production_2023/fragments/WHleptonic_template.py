import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
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
            processParameters = cms.vstring(
              'Check:event = off', #Might be needed, but it seems to run without
              'HiggsSM:all = off', # Other Higgs channels off
              'HiggsSM:ffbar2HZ = off', # ZH production
              'HiggsSM:ffbar2HW = on', # WH productio              
              '25:m0 = {[MHIGGS]}', # Mediator is SM Higgs. Current for ggF: 125,200,300,400,750,1000
              '24:onMode = off',
              '24:onIfAny = 11 13 15', #Leptonic decays
              '24:mMin = 0.1',
              '999999:all = GeneralResonance void 0 0 0 {[MDARK]} 0.001 0.0 0.0 0.0', # The dark meson definition: name, antiname, spin=2s+1 (0=undef), charge*3, color (0=single, 1=triplet, 2=octet), m0, width, mMin, mMax, tau
              '999998:all = GeneralResonance void 1 0 0 {[MPHO]} 0.001 0.0 0.0 0.0', # A dark boson which is a color triplet
              '999999:addChannel = 1 1.0 101 999998 999998 ', # First dark particle decays to a pair of the second
              {[DECAYS]}
            ),
            parameterSets = cms.vstring('pythia8CommonSettings',
                                        'pythia8CP5Settings',
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
