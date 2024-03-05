Welcome and thanks for choosing the ECALpro tools!

Download:
```
cmsrel CMSSW_13_3_0_pre3  
cd CMSSW_13_3_0_pre3/src
cmsenv
git cms-init
git clone --branch 133X -o pi0_cbasile https://github.com/BasChiara/ECALpro.git CalibCode
scram b -j16
```
This repo is set up to produce 2023 pi0 ICs for final rereco (04/03/2024). Just lounch the commands:
```
cd CalibCode/submit
./submitCalibrationCondor.py -l
```
Intro:

To get IC you basically need only to do 2 things:
1) Set the file parameters.py with the right values
2) lounce the command: "./submitCalibrationCondor.py -l"

------
1a) parameters.py
It contains all parameters define yout IC, divided id:
 a) Calib parameter: Name of directories, output names, how to split jobs, the queues.
       This is the first part of the file. in general is commnted the meaning of the variable, so it is easy to understand.
 b) IC parameter: selection cuts, Name of the dataset, json files, Global Tag, Laser correction, adcToGev Tag ecc...
       This is easy to choose, because they are in the last part of the file, and just decommenting the part of the dataset you need you will have all consistent values.

1b) Purify_List.py
It take the list of input root file and using the json file it creates a purified list of files.
>python Purify_List.py

------
2) submitCalibration.py
It creates all the directories and the cfg/sh files you need to run the calibration (using the functions in method.py). At the end of the process it will launche the DEAMON. This
controll all the others, waiting that they finish to proced with further steps.
In general you:
 -> Run the FillEpsilonPlot modules on ALL the jobs: this give you output called "TAGname_EcalNtp_x.root", where x is the number of the job.
 -> When ALL thos jobs sre finished the DEAMON send hadd jobs to merge them all ina  single file called "TAGname_epsilonPlots.root"
 -> Then the DEAMON launch the FIT modules in this file, that contain all the statistic: each job has the following output "TAGname_Endcap_x_calibMap.root" or "TAGname_Barrel_x_ca
 -> Once all the jobs are done the DEAMON will merge all the output using pyroot (not sending a job). The final output is: "TAGname_calibMap.root"
At the end of the calibration is good to remove all the log file "rm -rf directory/log/*log", and all the file on EOS that are merged.
I suggest you to use ThePerfectBashScript.sh in Utilities to do that.

------
3) After calibration:
When calibration is finished you can work in your IC, and print teh IC.txt used to crate a TAG with your IC.
 a) You can start checking if the IC are converged using the "Convergence.C" in AfterCalibTools/TestConvergence.
    doing:
      gROOT->ProcessLine(".include /afs/cern.ch/cms/slc5_ia32_gcc434/lcg/roofit/5.26.00-cms5/include")
      .x Convergence.C+("/store/group/alca_ecalcalib/lpernie/","directory",nIter,"TAGname")
    you your see that the RMS of the IC iter by iter decreas gradually under the per mill.
 b) Then you want to applky the residual correction from 2010 using "Residual.C". Residual are final correction to recover what Containment correction are not correcting.
    To do that you need to have IC derived on 2010 with the same selection you are using on your dataset:
    (I have it and is /store/group/alca_ecalcalib/lpernie/ALL_2010_WithNEWSelection_02/iter_13/calibMap.root).
 c) Then you want to get the ABSOLUTE IC (now your IC are relative to the IC used to create your ALCA file of input). To do that you have to moltiply your IC for the IC used previ
    You can do that for istance: "python MoltiplicateIC.py InputFile/EcalIntercalibConstants_GR10_H_V6.xml 2010/IC_ResidsualFree.root 2010/ABSIC_ResidsualFree.root"
    in InputFile there are all the IC at HLT stage for different period, if something is missing you can use the READGT tools to get it.
 d) Then you want to mediate your IC to 1. You can do that Globally for EB and EE separated, or for EtaRing. This will give you a .txt file with the IC you want to test.
 
------
4) Statistical Error
TO combine your IC with other IC, you need to provide a systematic and statistic error. The second one os computed re-running the last iter of a calibration twice.
Once only on even events, the others on odd events.Then from the difference/4 of a single IC, you can have the stat. error on it.
To do that you have to resubmit the calibration twice, but before remember to make news directories on EOS to store the IC running on all events, the odd and even one.
The command is
./resubmitCalibration.py iteration_to_resume 1 False False (for even events) and when it is finished
./resubmitCalibration.py iteration_to_resume 2 False False (for odd events)
Once you have the 2 sets of IC you can use: "python ComputeStatErr.py File_even.root File_odd.root Output.root"

5-extra) RESUME a calibration
Could happen that a calibration dies. Because some internal error, because of EOS, because you kill a job for error.
You can resubmit the Calibration from the iter you need:
./resubmitCalibration.py iteration_to_resume 0 False False
if you have the "TAGname_epsilonPlots.root" file you can directly resubmit the FIT part, jumping the first part:
./resubmitCalibration.py iteration_to_resume 0 True False
En if also the FIT is done you can only do the final merge:
./resubmitCalibration.py iteration_to_resume 0 True True
If you have all the "TAGname_EcalNtp_x.root" files, but not the final "TAGname_epsilonPlots.root", you can do by your own the hadd and tehn resubmit for the fit.
To do by your own check "bash ThePerfectBashScript.sh --help"

------
For more questions: luca.pernie@cern.ch

Best,
LP
