import ROOT, os, sys, re, array, math
import time

ROOT.gROOT.SetBatch(True)

absoluteIC = 1
outpath = "/afs/cern.ch/user/m/mciprian/www/pi0calib/ICplot_Legacy/ratioIC/"
outpath = "/eos/user/c/cbasile/www/CalibPi0_Run3/ICratios/Pi022wrtPi018/"
#outdir = "AlCaP0_AllRun2017_condor_iter1__Over__AlCaP0_Run2017_DE_run304366_ContCorrEoverEtrueScaledToV2MC_ext1_fromIter6_iter6/"
outdir = "/AlCaP0_2022BE_vs_AlCaP0_2018_ULrereco_1every2/"
canvasSuffix = "ratioIC"
#label1 = "2018 UL (half 2018, ~30 fb^{-1 })"
#label2 = "2018 test (other half, ~30 fb^{-1 })"
label1 = "2022 B/C/D/E"
#label1 = "2022 F/G"
label2 = "2018UL (half 2018, ~30 fb^{-1 })"
    
f1 = "/eos/user/c/cbasile/www/CalibPi0_Run3/AlCaP0_2022BE_TestCalib_iter8to10/iter_2/2DMaps/ICmaps/calibrationMaps.root"
#f1 = "/eos/user/c/cbasile/www/CalibPi0_Run3/AlCaP0_2022FG_TestCalib_iter5to10/iter_5/2DMaps/ICmaps/calibrationMaps.root"
f2 = "/eos/user/c/cbasile/www/CalibPi0_Run3/Run2_2018/AlCaP0_2018_ULrereco_1every2_ext1_fromIter6/iter_3/2DMaps/ICmaps/calibrationMaps.root"

n1 = { "EB"  : "calibMap_EB",
       "EEp" : "calibMap_EEp",
       "EEm" : "calibMap_EEm"
       }

n2 = { "EB"  : "calibMap_EB",
       "EEp" : "calibMap_EEp",
       "EEm" : "calibMap_EEm"
       }

if absoluteIC:
    outdir += "absolute/"
    for key in n1:
        n1[key] += "_absolute"
    for key in n2:
        n2[key] += "_absolute"
else:
    outdir += "normalized_final/"

rangeIC = { "EB"  : [0.95, 1.05],
            "EEp" : [0.9, 1.1],
            "EEm" : [0.9, 1.1]
            }

numDet = { "EB"  : 0,
           "EEp" : 1,
           "EEm" : 2
           }

outfull = outpath + outdir

print ("="*30)

for det in n1:

    cmd = "root -l -b -q 'makeICratio.C++(\"{out}\",\"{cs}\",\"{f1}\",\"{f2}\",\"{n1}\",\"{n2}\",{minIC},{maxIC},{nDet},\"{l1}\",\"{l2}\")'".format(out=outfull, 
                                                                                                                                                    cs=canvasSuffix, 
                                                                                                                                                    f1=f1, f2=f2, 
                                                                                                                                                    n1=n1[det], n2=n2[det], 
                                                                                                                                                    minIC=rangeIC[det][0], 
                                                                                                                                                    maxIC=rangeIC[det][1],
                                                                                                                                                    nDet=numDet[det],
                                                                                                                                                    l1=label1,
                                                                                                                                                    l2=label2)
    print ("-"*30)
    print (">>> " + det)
    print (cmd)
    os.system(cmd)


print ("="*30)
print ("THE END")
print ("="*30)


