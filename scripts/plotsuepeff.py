"""
    Light-weight plotter for VBF SUEP MC samples in 2023.
    Raymond Kil, 2024
"""

import json
import mplhep as hep
import matplotlib.pyplot as plt
import definitions as vbf
from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")

parser.add_option("--jsonpath"   , dest="jsonpath"   , default="./"    , help="directory where the quantity json files are.")
parser.add_option("--outputdir"  , dest="outputdir"  , default="./"    , help="plot output directory")
(options, args) = parser.parse_args()

outputdir   = options.outputdir
jsonpath    = options.jsonpath

jsonfile = json.load(open(jsonpath,'r'))
denom, numer = jsonfile['denominator'], jsonfile['numerator']

if   'pt105' in jsonpath: triggerpath = 'HLT_VBF_DiPFJet105_40_Mjj1000_Detajj3p5'
elif 'pt125' in jsonpath: triggerpath = 'HLT_VBF_DiPFJet125_45_Mjj720_Detajj3p0'

if 'tight' in jsonpath: triggerpath += ' (tight)'
else: triggerpath += ' (loose)'

if 'leadpt' in jsonpath:
    binsize = 5
    maxbin  = 300
    xlabel  = r"$p_T^{leadjet}$ [GeV]"
    plotname = 'leadpt'
    threshold = 105 if 'pt105' in jsonpath else 125
elif 'mjj' in jsonpath:
    binsize = 50
    maxbin  = 3000
    xlabel  = r"$M_{jj}$ [GeV]"
    plotname = 'mjj'
    threshold = 1000 if 'pt105' in jsonpath else 720
elif 'deta' in jsonpath:
    binsize = 0.1
    maxbin  = 7
    xlabel  = r"$\Delta\eta (j_1,j_2)$"
    plotname = 'deta'
    threshold = 3.5 if 'pt105' in jsonpath else 3.0


plt.style.use(hep.style.CMS)
fig = plt.figure()
effs, yerrmin, yerrmax, bincenters = vbf.GetEfficiency(binsize, maxbin, numer, denom)
plt.errorbar(bincenters, effs, yerr=[yerrmin,yerrmax], xerr=binsize, marker='o', linestyle='', label=triggerpath)
plt.xlabel(xlabel)
plt.ylabel('Efficiency')
plt.ylim(-0.05,1.1)
hep.cms.text("Simulation")
plt.axvline(x=threshold, color='r', label="Threshold", linestyle="--")
plt.legend(loc=2, fontsize='15')
plt.grid()
#hep.cms.lumitext(r"$L=21.70 \,fb^{-1}$ 2023 (13.6 TeV)")
plt.savefig(f"{outputdir}M125genericT2_{plotname}_pt105_tight.png")