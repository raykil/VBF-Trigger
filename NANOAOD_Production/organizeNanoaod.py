"""
    This script performs various jobs organizing nanoaod files. The list of functions are:
        - rename_files: Introducing placeholder zeros in nanoaod file names. For example, nanoaod_49.root becomes nanoaod_0049.root. This is easier for file management.
        - check_missing_files: There are some missing nanoaod files for various reasons. Checks the missing files and saves the names in a text file. Total number of files is 5442, from 0 to 5441.
        - log_check: Checking the log files for each nanoaod file to see if the nanoaod is successfully made. Makes three text files -- complete, incomplete, whatisthis -- according to log status.
        - remove_incomp: Based on incomplete file list from log_check, remove the corresponding incomplete files.
"""
import os
import numpy as np

rename_files = True
check_missing_files = True
log_check = True
remove_incomp = True

###### Rename Files ######
if rename_files:
    aodpath  = "/eos/user/j/jkil/SUEP/suep-production/2023C_mu_NANOAOD_withJetFB/NANOAOD/"
    aodfiles = [x for x in os.listdir(aodpath) if "nanoaod" in x]
    for idx, aodfile in enumerate(aodfiles):
        if idx%10==0: print(f"renaming the file {aodfile}")
        if aodfile[9]==".":
            os.system(f"mv {aodpath}{aodfile} {aodpath}nanoaod_000{aodfile[8]}.root")
        elif aodfile[10]==".":
            os.system(f"mv {aodpath}{aodfile} {aodpath}nanoaod_00{aodfile[8:10]}.root")
        elif aodfile[11]==".":
            os.system(f"mv {aodpath}{aodfile} {aodpath}nanoaod_0{aodfile[8:11]}.root")
        else:
            continue

###### Checking Missing Files ######
if check_missing_files:
    print("starting check_missing_files!")
    aodpath  = "/eos/user/j/jkil/SUEP/suep-production/2023C_mu_NANOAOD_withJetFB/NANOAOD/"
    aodfiles = [x for x in os.listdir(aodpath) if "nanoaod" in x]
    aodnums = []
    missingfiles = []
    exhaustive = np.arange(0,5442, dtype=int)

    for aodfile in aodfiles:
        aodnums.append(int(aodfile[8:12]))
    
    for e in exhaustive:
        if e not in aodnums: missingfiles.append(f"nanoaod_{e}.root")
    
    with open("missingfiles.txt", 'w') as m:
        for missingfile in missingfiles:
            m.write(str(missingfile)+'\n')
            

###### Log Check ######
if log_check:
    path = "/eos/user/j/jkil/SUEP/suep-production/2023C_mu_NANOAOD_withJetFB/eosbatchlogs/"
    logfiles = [x for x in os.listdir(path) if "nanoaod" in x]
    completed_files, incomplete_files, what_is_this = [], [], []

    print("started looking at log files...")
    for logfile in logfiles:
        print("processing : {}".format(logfile))
        with open(path+logfile, 'r') as l:
            if os.path.getsize(path+logfile)<10:
                incomplete_files.append(logfile)
            else:
                final_line = l.readlines()[-2]
                if "- Number of" in final_line:
                    completed_files.append(logfile)
                elif "Begin processing" in final_line:
                    incomplete_files.append(logfile)
                else:
                    what_is_this.append(logfile)

    with open("completed_files.txt", 'w') as c:
        c.write("completed_files!!\n")
        for line in completed_files:
            c.write(line+"\n")
    print("completed_files written!")

    with open("incomplete_files.txt", 'w') as i:
        i.write("incomplete_files!!\n")
        for line in incomplete_files:
            i.write(line+"\n")
    print("incomplete_files written!")

    with open("what_is_this.txt", 'w') as w:
        w.write("what_is_this!!\n")
        for line in what_is_this:
            w.write(line+"\n")
    print("what_is_this written!")

###### Remove Incomplete Files ######
if remove_incomp:
    path = "/eos/user/j/jkil/SUEP/suep-production/2023C_mu_NANOAOD_withJetFB/incomplete_files.txt"
    rootdir = "/eos/user/j/jkil/SUEP/suep-production/2023C_mu_NANOAOD_withJetFB/NANOAOD/"
    rootfiles = [x for x in os.listdir(rootdir) if "nanoaod" in x]

    with open(path, 'r') as f:
        incomplete_files = f.readlines()

    for item in incomplete_files:
        item = item[:-3]

    print(incomplete_files)

    for rootfile in incomplete_files:
        print("rm {}".format(rootdir+rootfile))
        os.system("rm {}".format(rootdir+rootfile))