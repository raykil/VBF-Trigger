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
              #'Check:event = off', #Might be needed, but it seems to run without
              'HiggsSM:all = off', # Other Higgs channels off
              'HiggsSM:gg2H = on', # ZZ VBF production
              '25:m0 = {[MHIGGS]}', # Mediator is SM Higgs. Current for ggF: 125,200,300,400,750,1000
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



#     Filter setup
# ------------------------
# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/PhysicsTools/HepMCCandAlgos/python/genParticles_cfi.py
process.tmpGenParticles = cms.EDProducer("GenParticleProducer",
    saveBarCodes = cms.untracked.bool(True),
    src = cms.InputTag("generator","unsmeared"),
    abortOnUnknownPDGCode = cms.untracked.bool(False)
)

# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoJets/Configuration/python/GenJetParticles_cff.py
# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoMET/Configuration/python/GenMETParticles_cff.py
process.tmpGenParticlesForJetsNoNu = cms.EDProducer("InputGenJetsParticleSelector",
    src = cms.InputTag("tmpGenParticles"),
    ignoreParticleIDs = cms.vuint32(
         1000022,
         1000012, 1000014, 1000016,
         2000012, 2000014, 2000016,
         1000039, 5100039,
         4000012, 4000014, 4000016,
         9900012, 9900014, 9900016,
         39,12,14,16),
    partonicFinalState = cms.bool(False),
    excludeResonances = cms.bool(False),
    excludeFromResonancePids = cms.vuint32(12, 13, 14, 16),
    tausAsJets = cms.bool(False)
)

# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoJets/JetProducers/python/AnomalousCellParameters_cfi.py
process.AnomalousCellParameters = cms.PSet(
    maxBadEcalCells         = cms.uint32(9999999),
    maxRecoveredEcalCells   = cms.uint32(9999999),
    maxProblematicEcalCells = cms.uint32(9999999),
    maxBadHcalCells         = cms.uint32(9999999),
    maxRecoveredHcalCells   = cms.uint32(9999999),
    maxProblematicHcalCells = cms.uint32(9999999)
)

# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoJets/JetProducers/python/GenJetParameters_cfi.py
process.GenJetParameters = cms.PSet(
    src            = cms.InputTag("tmpGenParticlesForJetsNoNu"),
    srcPVs         = cms.InputTag(''),
    jetType        = cms.string('GenJet'),
    jetPtMin       = cms.double(3.0),
    inputEtMin     = cms.double(0.0),
    inputEMin      = cms.double(0.0),
    doPVCorrection = cms.bool(False),
    # pileup with offset correction
    doPUOffsetCorr = cms.bool(False),
       # if pileup is false, these are not read:
       nSigmaPU = cms.double(1.0),
       radiusPU = cms.double(0.5),  
    # fastjet-style pileup     
    doAreaFastjet  = cms.bool(False),
    doRhoFastjet   = cms.bool(False),
      # if doPU is false, these are not read:
      Active_Area_Repeats = cms.int32(5),
      GhostArea = cms.double(0.01),
      Ghost_EtaMax = cms.double(6.0),
    Rho_EtaMax = cms.double(4.5),
    useDeterministicSeed= cms.bool( True ),
    minSeed             = cms.uint32( 14327 )
)

# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoJets/JetProducers/python/ak4GenJets_cfi.py
process.tmpAk4GenJetsNoNu = cms.EDProducer(
    "FastjetJetProducer",
    process.GenJetParameters,
    process.AnomalousCellParameters,
    jetAlgorithm = cms.string("AntiKt"),
    rParam       = cms.double(0.4)
)

process.genHTFilter = cms.EDFilter("GenHTFilter",
   src = cms.InputTag("tmpAk4GenJetsNoNu"), #GenJet collection as input
   jetPtCut = cms.double(30.0), #GenJet pT cut for HT
   jetEtaCut = cms.double(2.5), #GenJet eta cut for HT
   genHTcut = cms.double({[HTCUT]}) #genHT cut
)

