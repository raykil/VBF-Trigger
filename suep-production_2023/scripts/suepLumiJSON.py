"""
    Light-weight suep luminosity calculation.
    Raymond Kil, 2024
"""

import uproot
import os
import numpy as np

path = '/eos/user/j/jkil/vbftrigger/suep-production_2023/M125genericT2/jobs/output/nanoaod/nanoaod_002.root'
path = 'root://cms-xrd-global.cern.ch///store/data/Run2023C/Muon0/NANOAOD/PromptNanoAODv12_v3-v1/2820000/27a91d41-f47a-4beb-a99e-d76b942c4477.root'
with uproot.open(path) as nanoaod:
    luminosities = nanoaod["LuminosityBlocks"]
    run, lum = luminosities["run"].array(), np.array(luminosities["luminosityBlock"].array(),dtype='int')
    print('GenFilter_filterEfficiency     ', luminosities['GenFilter_filterEfficiency'].array())
    print('GenFilter_filterEfficiencyError', luminosities['GenFilter_filterEfficiencyError'].array())
    print('GenFilter_numEventsPassed      ', luminosities['GenFilter_numEventsPassed'].array())
    print('GenFilter_numEventsTotal       ', luminosities['GenFilter_numEventsTotal'].array())
    print('run', run)
    print('lum', lum)
