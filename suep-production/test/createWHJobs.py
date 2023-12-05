
baseoutputdir = "/eos/user/j/jreicher/SUEP/WH_private_signals/"
base = "python submitJobs.py  --channel WHleptonic --decay generic -T [T] -M [M] --decay [DECAY] --mDark [MDARK]  --toSave NANOAOD --batch condor --outputdir %s -j 40 -e 1000 --year [YEAR]"%baseoutputdir

params = {
        "mS": [125],
        "mPhi": [1,2,3,4,8],
        "TovermPhi": [0.25,0.5,1,2,4],
        "decays": ["generic", "leptonic", "hadronic"],
        "year": ["UL18", "UL17", "UL16", "UL16APV"],
}
# A decay mode sets a mass of the dark photon
mA = {"leptonic": 0.5, "hadronic": 0.7, "generic": 1.}

# Dict of all T slices
points = {}
for year in params["year"]:
    for mS in params["mS"]:
        for mPhi in params["mPhi"]:
            for TovermPhi in params["TovermPhi"]:
                for decaymode in params["decays"]:
                    mAHere = mA[decaymode]
                    mPhiHere   = max(mAHere*2, mPhi)
                    T = TovermPhi*mPhiHere
                    # Splitting in T is really only useful when dealing with central scans, but keep the logic to avoid duplicating points at low mdark
                    if not T in points.keys():
                        points[T]    = []
                    newname = "SUEP_mS%1.3f_mPhi%1.3f_T%1.3f_mode%s_%s"%(mS, mPhiHere, T, decaymode, year)
                    add = True
                    for other in points[T]:
                        if "name" in other:
                            if newname ==  other["name"]:
                                add = False
                    if not(add): continue
                    print(base.replace("[M]", "%1.1f"%mS).replace("[DECAY]", decaymode).replace("[MDARK]", "%1.2f"%mPhiHere).replace("[T]", "%1.2f"%T).replace("[YEAR]", year))
                    points[T].append({"name" : newname})
