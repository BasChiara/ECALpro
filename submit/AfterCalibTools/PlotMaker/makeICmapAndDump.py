import ROOT, os, sys, re, array, math
import os, sys, re, array, math
import time

#ROOT.gROOT.SetBatch(True)

Run2 = True

foldername = "AlCaP0_2022FG_TestCalib_iter5to10"
if Run2 : foldername = "AlCaP0_2018_ULrereco_1every2_ext1_fromIter6"
niter = 3       # generally it starts from 0
eosPi0Folder = "pi0"
if Run2 : eosPi0Folder = "piZero_Run2/mciprian"
excludeMod2EBm16 = True
excludeMod4EBm06 = True if "2016" in foldername else False # might also have iphi in 41-60

outpath = "/eos/user/c/cbasile/www/CalibPi0_Run3/"
if Run2 : outpath = "/eos/user/c/cbasile/www/CalibPi0_Run3/Run2_2018/"
outfull = outpath + foldername + "/iter_" + str(niter) + "/2DMaps/ICmaps/"

f1 = "/eos/cms/store/group/dpg_ecal/comm_ecal/{eosfd}/{fd}/iter_{n}/{fd}_calibMap.root".format(eosfd=eosPi0Folder,
                                                                                                     fd=foldername, 
                                                                                                     n=niter)
if Run2 :
    f1 = "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/{eosfd}/{fd}/iter_{n}/{fd}_calibMap.root".format(eosfd=eosPi0Folder,
                                                                                                     fd=foldername, 
                                                                                                     n=niter)

print ("="*30)

cmd = "root -l -b -q 'makeICmapAndDump.C++(\"{out}\",\"{f1}\",\"dumpIC_norm1etaRing.dat\",\"calibMap_EB\"".format(out=outfull, 
                                                                                                                  f1=f1)
                                                                                           
cmd += ", 0.95, 1.05,true,false,0,{ex1},{ex2})'".format(ex1="true" if excludeMod2EBm16 else "false",
                                                        ex2="true" if excludeMod4EBm06 else "false")


print ("-"*30)
print (cmd)
os.system(cmd)


print ("="*30)
print ("THE END")
print ("="*30)


