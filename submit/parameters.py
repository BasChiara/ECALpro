#Do not modify these
nEventsPerJob      = '-1'
outputFile         = 'EcalNtp'           # without .root suffix
calibMapName       = 'calibMap.root'
GeometryFromFile   = False               # Keep that False, you want the cmssw geometry. Anyway the geometry file is needed
ExternalGeometry   = 'caloGeometry.root' 
CalibType          = 'xtal'              # Calibrating single xtals. I never try but you could calibrate EtaRing ot Trigger Towers

#Are Pi0
Are_pi0            = True               # True = using Pi0, False = using Eta
#Fold per Eta Ring
EtaRingCalibEB     = False
SMCalibEB          = False
EtaRingCalibEE     = False
SMCalibEE          = False
CalibMapEtaRing    = "CalibCode/FillEpsilonPlot/data/calibMap.root"
FixGhostDigis      = False   # this parameter is useful only for 2015. In 2016 stream the ghosts are no more there, but this is not harmful (can stay True)

#PATH
eosPath =  '/eos/cms/store/group/dpg_ecal/comm_ecal/pi0'
#
prefixSourceFile = 'root://cms-xrd-global.cern.ch/'  # last / is left on purpose; tipically it can be '', but if source files are not on eos you need this prefix in PoolSource
#  
#CRAB
isCRAB           = False               # If not is batch
CRAB_Data_Path   = '/SinglePion_FlatPt-1To15_AsymptNoPU/emanuele-SinglePion_FlatPt-1To15_AsymptNoPU-9709e5e865f17288f5a53621cf8e9935/USER'
CRAB_CopyCert    = '/afs/cern.ch/user/l/lpernie/private/x509up_u12147'
storageSite      = "T2_CH_CERN"
unitsPerJob = 50   #DBS File per Job
isOtherT2        = False
#MC and Selection Optimization
isDebug = False # for the moment, if True it activates some cout in FillEpsilonPlot.cc
isMC = False
isMCV1 = False  # use V1 MC, otherwise V2 (some options are changed automatically below). It was for 2017 to make the CC, we had 2 different MC
useMassInsteadOfEpsilon = True # when doing calibration with mass, use the mass instead of its ratio with the nominal one (can stay True even if isEoverEtrue is True)
isEoverEtrue = False if isMC==False else True # automatically set to False if isMC is False, otherwise it runs the E/Etrue study to get the containment corrections
#localFolderToWriteFits = "/afs/cern.ch/work/m/mciprian/ecalpro_stuff/fits" if isEoverEtrue else ""  # no ending / needed
localFolderToWriteFits = ""  # keep empty if not used, but in any case it only works if isEoverEtrue=True
# if isEoverEtrue is set to False for MC, it runs the usual pi0 intercalibration using the mass
MakeNtuple4optimization = False
useCalibrationSelection = False # to use same selection of calibration when making ntuples (so not to copy all the cuts)
useStreamSelection = False   # for now it only work with MakeNtuple4optimization = True, otherwise it is ignored, it is a hardcoded way to use the stream selection below
#InputList and Folder name
inputlist_n      = 'InputList/purified_AlCaP0_Run2022BG_29_07_2023.list' if isMC==False else 'InputList/MultiPion_FlatPt-1To15_PhotonPtFilter_RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2.list'
dirname          = 'AlCaP0_2022BG_onlyEE_TestCalib' if isMC==False else 'pi0CC_2018_EoverEtrue_foldSM_nFit10_onlyEB_fixGamma2EoverEtrue'   #'pi0Gun_MCV2_EoverEtrue_foldSM' #'testMC_adirname          = 'AlCaEta_2018_tagAsPi0ForULcalibration_ntuplesOptim' if isMC==False else 'pi0CC_2018_EoverEtrue_foldSM_nFit10_onlyEB_fixGamma2EoverEtrue'   #'pi0Gun_MCV2_EoverEtrue_foldSM' #'testMC_all_v2' #'AlCaP0_IC2017_upTo21September2017_2012regression_v2' # 'test' 
NameTag          = dirname+'_' # Tag to the names to avoid overlap
Silent           = False                 # True->Fill modules is silent; False->Fill modules has a standard output

# to manage storing of rechits on eos, to avoid running unpacker and local reconstruction (multifit) for each iteration
justCreateRecHits = False # if True, will run one iteration to produce and store RecHits from Digis
runCalibrationFromRecHits = False # run calibration from rechits (it disables FROMDIGI below), it works if you have already run with justCreateRecHits = True
eosOutputPathForRecHits = "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/piZero_Run3/emanuele" # the path on eos where RecHits are stored (a subfolder named as 'AlCaP0_RecHitsFromDigis_dirname' is created)
filterEventsByAlCaTrigger = True # filter away pi0 or eta depending on what we will use (modest gain in speed for pi0, but huge for eta since number of events is much less). 
# Might also filter by EB or EE (useful if one wants to run only on one of them) according to 'Barrel_or_Endcap' below, but not yet implemented since barrel is more important and has almost all the statistics

#####
#
# old queues for lxbatch, obsolete, should be removed
queueForDaemon   = 'cmscaf1nw'          # Option suggested: 2nw/2nd, 1nw/1nd, cmscaf1nw/cmscaf1nd... even cmscaf2nw
queue            = 'cmscaf1nd'
#############

#ITERS
nIterations      = 5 if isMC==False else 1 # 7
if justCreateRecHits:
   nIterations = 1
if MakeNtuple4optimization:
   nIterations = 1
#nThread          = 4 # if bigger than 1, enable multithreading, but I'm not sure if ECALpro supports it (see methods.py searching nThread)

SubmitFurtherIterationsFromExisting = True
# maybe I don't need the root://eoscms/ prefix if eos is mounted
startingCalibMap = '/eos/cms/store/group/dpg_ecal/comm_ecal/pi0/AlCaP0_2022FG_TestCalib_iter5to10/iter_5/AlCaP0_2022FG_TestCalib_iter5to10_calibMap.root'
# used  only if SubmitFurtherIterationsFromExisting is True
SystOrNot = 0 # can be 0, 1 or 2 to run on all (default), even or odd events. It works only if you submit this new iteration from an existing one, therefore SubmitFurtherIterationsFromExisting must be set true. Tipically 0 is the default and has no real effect, it is like submitting usual iterations.  

#N files
ijobmax          = 10 if isMC==False else 1  # 5 number of files per job, 1 for MC to avoid loosing too many events due to problematic files
if justCreateRecHits:
   ijobmax = 1 # when recreating rechits from digis, keep same correspondance of files 
nHadd            = 35 #35                    # 35 number of files per hadd
nFit             = 2000 if isMC==False else 10                 # number of fits done in parallel
useFit_RooMinuit = False if isEoverEtrue else True # if True the fit is done with RooMinuit, otherwise with RooMinimizer. The former is obsolete, but the latter can lead to a CMSSW error which makes the job fail, creating large white strips in the map. This happens often because the fit sees a negative PDF at the border of the fit range, RooFit will try to adjust the fit range to avoid the unphysical region, but after few trials CMSSW throws an error: without CMSSW the fit should actually be able to try several thousands of times before failing
# However, at least from CMSSW_10_2_X, for EoverEtrue with fits using RooCMSshape+double-Crystal-Ball the fits are much better, so let's use RooMinimizer in that case
Barrel_or_Endcap = 'ONLY_ENDCAP'          # Option: 'ONLY_BARREL','ONLY_ENDCAP','ALL_PLEASE'
ContainmentCorrection = 'EoverEtrue' # Option: 'EoverEtrue' , 'No'
copyCCfileToTMP = False  # copy file from eos to /tmp/, should make jobs faster
foldInSuperModule = False if isMC==False else True
fillKinematicVariables = True # fill some histograms with kinematic variables in FillEpsilonPlot.cc, you can disable this option to save storage space, but it is really a small fraction of the total size

#Remove Xtral Dead
RemoveSeedsCloseToDeadXtal = False # if True, require that the seed is at least 1 crystal far from dead zones (the 3x3 matrix does not contain dead crystals). However, it should be already done because the algorithm reject clusters with crystals woth channelstatus > 0 (as in the case of dead channels). Leave it False for now
RemoveDead_Flag = "True"
RemoveDead_Map  = ""
#RemoveDead_Map  = "/afs/cern.ch/work/l/lpernie/ECALpro/gitHubCalib/CMSSW_6_2_5/src/CalibCode/submit/AfterCalibTools/DeadXtals/plots/h_DeadXtal.root"

#L1 Bit Collection
L1TriggerInfo = False                            # If we want to Fill the L1 Trigger Bit Histo (and if we perform the cut based on a L1Bit of L1Seed != ""), to save L1 branches in ntuples MakeNtuple4optimization must be True
# you can have it True even for calibration, but it is not needed and just slow things down reading bits for each event
if MakeNtuple4optimization:
   #L1TriggerInfo = True
   L1TriggerInfo = False
L1Seed = ""                                         # You can ask that one Bit is FIRED: Ex: "L1_SingleJet16" or more complicated stuff "L1_SingleJet16 OR L1_SingleJet36" (to be implemented in FIllEpsilonPlots.cc

# copy paste here the list of seeds from the stream. It is used only if you decide to store L1 info in the ntuples produced by FillEpsilonPlots.cc
# L1TriggerInfo must be True to use this expression
# if L1TriggerInfo is false, an empty string is passed to FillEpsilonPlot, and the number of seeds is set to 1 (because it is used by an histogram than cannot have 0 bins)
L1SeedExpression = "L1_AlwaysTrue OR L1_IsolatedBunch OR L1_SingleEG8er2p5 OR L1_SingleEG10er2p5 OR L1_SingleEG15er2p5 OR L1_SingleEG26er2p5 OR L1_SingleEG34er2p5 OR L1_SingleEG36er2p5 OR L1_SingleEG38er2p5 OR L1_SingleEG40er2p5 OR L1_SingleEG42er2p5 OR L1_SingleEG45er2p5 OR L1_SingleEG60 OR L1_SingleIsoEG26er2p5 OR L1_SingleIsoEG28er2p5 OR L1_SingleIsoEG30er2p5 OR L1_SingleIsoEG32er2p5 OR L1_SingleIsoEG34er2p5 OR L1_SingleIsoEG24er2p1 OR L1_SingleIsoEG26er2p1 OR L1_SingleIsoEG28er2p1 OR L1_SingleIsoEG30er2p1 OR L1_SingleIsoEG32er2p1 OR L1_DoubleEG_22_10_er2p5 OR L1_DoubleEG_25_14_er2p5 OR L1_DoubleEG_25_12_er2p5 OR L1_SingleJet35 OR L1_SingleJet60 OR L1_SingleJet90 OR L1_SingleJet120 OR L1_SingleJet140er2p5 OR L1_SingleJet160er2p5 OR L1_SingleJet180 OR L1_SingleJet200 OR L1_DoubleJet40er2p5 OR L1_DoubleJet100er2p5 OR L1_DoubleJet120er2p5 OR L1_QuadJet60er2p5 OR L1_HTT120er OR L1_HTT160er OR L1_HTT200er OR L1_HTT255er OR L1_HTT280er OR L1_HTT320er "
# NOTE: leave a space at the end! It is needed to search a seed name in the string without ambiguity 
# for instance, if you look for 'L1_SingleJet16' in the string, it also matches 'L1_SingleJet160', while if you search for 'L1_SingleJet16 ' there is no ambiguity
# it also relies on a space between each name and the 'OR'

#Seeds (Comment if you want the standard cuts ones)
EB_Seed_E    = '0.5'
useEE_EtSeed = 'False'
EE_Seed_Et   = '0.0'
EE_Seed_E    = '1.0' #1.5 for 40PU25
#Selection
CutOnHLTIso = "True"
if(Are_pi0):
   #inner barrel
   Pi0PtCutEB_low = '2.0' #2.0
   gPtCutEB_low = '0.65' #0.65
   Pi0IsoCutEB_low = '0.2'
   Pi0HLTIsoCutEB_low = "0.5"
   nXtal_1_EB_low = '7'
   nXtal_2_EB_low = '7'
   S4S9_EB_low = '0.88' #0.83
   #outer barrel 
   Pi0PtCutEB_high = '1.75' # 1.75
   gPtCutEB_high = '0.65' #0.65
   Pi0IsoCutEB_high = '0.2'
   Pi0HLTIsoCutEB_high = '0.5'
   nXtal_1_EB_high = '7'
   nXtal_2_EB_high = '7'
   S4S9_EB_high = '0.9' #0.83
   #low eta EE
   Pi0PtCutEE_low = '3.75'
   gPtCutEE_low = '1.1'
   Pi0IsoCutEE_low = '0.2'
   Pi0HLTIsoCutEE_low = '0.5'
   nXtal_1_EE_low = '6'
   nXtal_2_EE_low = '6'
   S4S9_EE_low = '0.85'
   #high eta EE
   Pi0PtCutEE_high = '2.0'
   gPtCutEE_high = '0.95'
   Pi0IsoCutEE_high = '0.2'
   Pi0HLTIsoCutEE_high = '0.5'
   nXtal_1_EE_high = '6'
   nXtal_2_EE_high = '6'
   S4S9_EE_high = '0.92'
   if MakeNtuple4optimization and not useCalibrationSelection:
   #inner barrel
      Pi0PtCutEB_low = '0.0'
      gPtCutEB_low = '0.5'
      Pi0IsoCutEB_low = '0.0'
      Pi0HLTIsoCutEB_low = "0.5"
      nXtal_1_EB_low = '4'
      nXtal_2_EB_low = '4'
      S4S9_EB_low = '0.75'
      #outer barrel 
      Pi0PtCutEB_high = '0.0'
      gPtCutEB_high = '0.5'
      Pi0IsoCutEB_high = '0.0'
      Pi0HLTIsoCutEB_high = '0.5'
      nXtal_1_EB_high = '4'
      nXtal_2_EB_high = '4'
      S4S9_EB_high = '0.75'
      #low eta EE
      Pi0PtCutEE_low = '0.0'
      gPtCutEE_low = '0.5'
      Pi0IsoCutEE_low = '0.0'
      Pi0HLTIsoCutEE_low = '0.5'
      nXtal_1_EE_low = '4'
      nXtal_2_EE_low = '4'
      S4S9_EE_low = '0.75'
      #high eta EE
      Pi0PtCutEE_high = '0.0'
      gPtCutEE_high = '0.5'
      Pi0IsoCutEE_high = '0.0'
      Pi0HLTIsoCutEE_high = '0.5'
      nXtal_1_EE_high = '4'
      nXtal_2_EE_high = '4'
      S4S9_EE_high = '0.75'
      if useStreamSelection:
      #inner barrel
         Pi0PtCutEB_low = '2.0'
         gPtCutEB_low = '0.65'
         Pi0IsoCutEB_low = '0.0'
         Pi0HLTIsoCutEB_low = "0.5"
         nXtal_1_EB_low = '0'
         nXtal_2_EB_low = '0'
         S4S9_EB_low = '0.88'
      #outer barrel 
         Pi0PtCutEB_high = '1.75'
         gPtCutEB_high = '0.65'
         Pi0IsoCutEB_high = '0.0'
         Pi0HLTIsoCutEB_high = '0.5'
         nXtal_1_EB_high = '0'
         nXtal_2_EB_high = '0'
         S4S9_EB_high = '0.9'
      #low eta EE
         Pi0PtCutEE_low = '3.75'
         gPtCutEE_low = '1.1'
         Pi0IsoCutEE_low = '0.0'
         Pi0HLTIsoCutEE_low = '0.5'
         nXtal_1_EE_low = '0'
         nXtal_2_EE_low = '0'
         S4S9_EE_low = '0.85'
      #high eta EE
         Pi0PtCutEE_high = '2.0'
         gPtCutEE_high = '0.95'
         Pi0IsoCutEE_high = '0.0'
         Pi0HLTIsoCutEE_high = '0.5'
         nXtal_1_EE_high = '0'
         nXtal_2_EE_high = '0'
         S4S9_EE_high = '0.92'
#ETA
else:
   #inner barrel
   Pi0PtCutEB_low = '3.0'
   gPtCutEB_low = '1.0'
   Pi0IsoCutEB_low = '0.0'
   Pi0HLTIsoCutEB_low = "0.5"
   nXtal_1_EB_low = '7'
   nXtal_2_EB_low = '6'
   S4S9_EB_low = '0.85'
   #outer barrel 
   Pi0PtCutEB_high = '3.0'
   gPtCutEB_high = '1.0'
   Pi0IsoCutEB_high = '0.0'
   Pi0HLTIsoCutEB_high = '0.5'
   nXtal_1_EB_high = '7'
   nXtal_2_EB_high = '6'
   S4S9_EB_high = '0.85'
   #low eta EE
   Pi0PtCutEE_low = '3.0'
   gPtCutEE_low = '0.7'
   Pi0IsoCutEE_low = '0.0'
   Pi0HLTIsoCutEE_low = '0.5'
   nXtal_1_EE_low = '7'
   nXtal_2_EE_low = '6'
   S4S9_EE_low = '0.85'
   #high eta EE
   Pi0PtCutEE_high = '3.0'
   gPtCutEE_high = '0.6'
   Pi0IsoCutEE_high = '0.0'
   Pi0HLTIsoCutEE_high = '0.5'
   nXtal_1_EE_high = '7'
   nXtal_2_EE_high = '6'
   S4S9_EE_high = '0.85'
   # #inner barrel
   # Pi0PtCutEB_low = '1'
   # gPtCutEB_low = '.4'
   # Pi0IsoCutEB_low = '0.0'
   # Pi0HLTIsoCutEB_low = "999"
   # nXtal_1_EB_low = '0'
   # nXtal_2_EB_low = '0'
   # S4S9_EB_low = '0.6'
   # #outer barrel
   # Pi0PtCutEB_high = '1.0'
   # gPtCutEB_high = '.4'
   # Pi0IsoCutEB_high = '0.0'
   # Pi0HLTIsoCutEB_high = '999'
   # nXtal_1_EB_high = '0'
   # nXtal_2_EB_high = '0'
   # S4S9_EB_high = '0.6'
   # #low eta EE
   # Pi0PtCutEE_low = '1.0'
   # gPtCutEE_low = '.4'
   # Pi0IsoCutEE_low = '.0'
   # Pi0HLTIsoCutEE_low = '999'
   # nXtal_1_EE_low = '0'
   # nXtal_2_EE_low = '0'
   # S4S9_EE_low = '0.6'
   # #high eta EE
   # Pi0PtCutEE_high = '1.0'
   # gPtCutEE_high = '0.4'
   # Pi0IsoCutEE_high = '0.0'
   # Pi0HLTIsoCutEE_high = '999'
   # nXtal_1_EE_high = '0'
   # nXtal_2_EE_high = '0'
   # S4S9_EE_high = '0.6'
   if MakeNtuple4optimization and not useCalibrationSelection:
      #inner barrel
      Pi0PtCutEB_low = '1'
      gPtCutEB_low = '.4'
      Pi0IsoCutEB_low = '0.0'
      Pi0HLTIsoCutEB_low = "999"
      nXtal_1_EB_low = '0'
      nXtal_2_EB_low = '0'
      S4S9_EB_low = '0.6'
      #outer barrel
      Pi0PtCutEB_high = '1.0'
      gPtCutEB_high = '.4'
      Pi0IsoCutEB_high = '0.0'
      Pi0HLTIsoCutEB_high = '999'
      nXtal_1_EB_high = '0'
      nXtal_2_EB_high = '0'
      S4S9_EB_high = '0.6'
      #low eta EE
      Pi0PtCutEE_low = '1.0'
      gPtCutEE_low = '.4'
      Pi0IsoCutEE_low = '.0'
      Pi0HLTIsoCutEE_low = '999'
      nXtal_1_EE_low = '0'
      nXtal_2_EE_low = '0'
      S4S9_EE_low = '0.6'
      #high eta EE
      Pi0PtCutEE_high = '1.0'
      gPtCutEE_high = '0.4'
      Pi0IsoCutEE_high = '0.0'
      Pi0HLTIsoCutEE_high = '999'
      nXtal_1_EE_high = '0'
      nXtal_2_EE_high = '0'
      S4S9_EE_high = '0.6'
      if useStreamSelection:
      #inner barrel
         Pi0PtCutEB_low = '3.0'
         gPtCutEB_low = '0.65'
         Pi0IsoCutEB_low = '0.0'
         Pi0HLTIsoCutEB_low = "0.5"
         nXtal_1_EB_low = '0'
         nXtal_2_EB_low = '0'
         S4S9_EB_low = '0.9'
      #outer barrel 
         Pi0PtCutEB_high = '3.0'
         gPtCutEB_high = '1.4'
         Pi0IsoCutEB_high = '0.0'
         Pi0HLTIsoCutEB_high = '0.5'
         nXtal_1_EB_high = '0'
         nXtal_2_EB_high = '0'
         S4S9_EB_high = '0.9'
      #low eta EE
         Pi0PtCutEE_low = '3.0'
         gPtCutEE_low = '1.0'
         Pi0IsoCutEE_low = '0.0'
         Pi0HLTIsoCutEE_low = '0.5'
         nXtal_1_EE_low = '0'
         nXtal_2_EE_low = '0'
         S4S9_EE_low = '0.9'
      #high eta EE
         Pi0PtCutEE_high = '3.0'
         gPtCutEE_high = '1.0'
         Pi0IsoCutEE_high = '0.0'
         Pi0HLTIsoCutEE_high = '0.5'
         nXtal_1_EE_high = '0'
         nXtal_2_EE_high = '0'
         S4S9_EE_high = '0.9'

#containment corrections (these are set below)
useContainmentCorrectionsFromEoverEtrue = True
fileEoverEtrueContainmentCorrections = ""
# choose a scaling factor, if any, for E/Etrue CC (was needed for 2017 CC: 1.006 (1.01) for photon 2 (1))
#scalingEoverEtrueCC_g1 = '1.01' # for 2017
#scalingEoverEtrueCC_g2 = '1.006' # for 2017
scalingEoverEtrueCC_g1 = '1.0'  # for 2018  
scalingEoverEtrueCC_g2 = '1.0' # for 2018
#
if ContainmentCorrection == 'EoverEtrue':  # in this case it is better to undefine MVA_REGRESSIO in FillEpsilonPlot.h
   useContainmentCorrectionsFromEoverEtrue = True
   fileEoverEtrueContainmentCorrections = "root://eoscms//eos/cms/store/group/dpg_ecal/alca_ecalcalib/piZero_Run2/mciprian/pi0CC_2018_EoverEtrue_foldSM_nFit10_onlyEB_fixGamma2EoverEtrue/iter_0/pi0CC_2018_EoverEtrue_foldSM_nFit10_onlyEB_fixGamma2EoverEtrue_calibMap.root"
   #fileEoverEtrueContainmentCorrections = "root://eoscms//eos/cms/store/group/dpg_ecal/alca_ecalcalib/piZero2017/mciprian/pi0Gun_MC_EoverEtrue_foldSM_v4/iter_0/pi0Gun_MC_EoverEtrue_foldSM_v4_calibMap.root"
   #fileEoverEtrueContainmentCorrections = "/afs/cern.ch/user/m/mciprian/www/pi0calib/CC_EoverEtrue/product_CC/pi0Gun_MC_EoverEtrue_foldSM_v4_iter1/ContainmentCorrections_EoverEtrue.root"
   #fileEoverEtrueContainmentCorrections = "root://eoscms//eos/cms/store/group/dpg_ecal/alca_ecalcalib/piZero2017/mciprian/pi0Gun_MCV2_EoverEtrue_foldSM/iter_0/pi0Gun_MCV2_EoverEtrue_foldSM_calibMap.root"

Endc_x_y = 'Endc_x_y_ring.txt' # stored in CalibCode/FillEpsilonPlot/data/
# preshower
useOnlyEEClusterMatchedWithES = 'True'

#-----------------------------------------------------------------------------------

#####################
# if you don't want to overwrite the global tag, set overWriteGlobalTag = False, otherwise, it will be customized based on the following tags  
#####################
overWriteGlobalTag = False if isMC==False else False                                     # Allow to overwrite AlphaTag, Laser correction etc
PFRechitTagRecord='EcalPFRecHitThresholdsRcd';PFRechitTag='EcalPFRecHitThresholds_UL_2018_2e3sig';PFRechitDB='frontier://FrontierProd/CMS_CONDITIONS'
laserTagRecord='EcalLaserAPDPNRatiosRcd';laserTag='EcalLaserAPDPNRatios_rereco2018_v3';laserDB='frontier://FrontierProd/CMS_CONDITIONS'            
alphaTagRecord='';alphaTag='';alphaDB=''
GeVTagRecord='';GeVTag='';GeVDB=''
pulseShapeTagRecord='EcalPulseShapesRcd';pulseShapeTag='EcalPulseShapes_UltraLegacy2018_calib';pulseShapeDB='frontier://FrontierProd/CMS_CONDITIONS'
pedestalTagRecord='EcalPedestalsRcd';pedestalTag='EcalPedestals_timestamp_2018_18January2019_collisions_blue_laser';pedestalDB='frontier://FrontierProd/CMS_CONDITIONS'
laserAlphaTagRecord='EcalLaserAlphasRcd';laserAlphaTag='EcalLaserAlphas_EB152-150_EEoptimized18';laserAlphaDB='frontier://FrontierProd/CMS_CONDITIONS'
ESIntercalibTagRecord='';ESIntercalibTag='';ESIntercalibDB='frontier://FrontierProd/CMS_CONDITIONS'
ESEEIntercalibTagRecord='';ESEEIntercalibTag='';ESEEIntercalibDB='frontier://FrontierProd/CMS_CONDITIONS'
intercalibTagRecord='EcalIntercalibConstantsRcd';intercalibTag='EcalIntercalibConstants_Run2018ABCD_run297056_eopPNEB_v1';intercalibDB='frontier://FrontierProd/CMS_CONDITIONS'
linearCorrectionsTagRecord='';linearCorrectionsTag='';linearCorrectionsDB='frontier://FrontierProd/CMS_CONDITIONS'
EcalChannelStatusTagRecord='EcalChannelStatusRcd';EcalChannelStatusTag='EcalChannelStatus_v13_offline';EcalChannelStatusDB='frontier://FrontierProd/CMS_CONDITIONS'


######################################################################
# Now decomment the part that correspond to data you want to run on. #
######################################################################

isNot_2010         = 'True'                                    # Fit Parameter Range
HLTResults         = 'True' if isMC==False else 'False'                                  # Fill the EB(EE) histos only is Eb()ee is fired: it uses GetHLTResults(iEvent, HLTResultsNameEB.Data() );
json_file          = ''
#json_file          = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt' if isMC==False else '' 
useJsonFilterInCpp = False  # True: use json filter in cfg python wrapper calling FillEpsilonPlots.cc; True: use json filter inside FillEpsilonPlots.cc
doEnenerScale      = 'False'
doIC               = 'False'                                   # Member of Recalibration Module
doLaserCorr        = "False"
#hltGtDigis         = 'InputTag("simGtDigis")'        # obsolete, not used in the Fill.cc   
triggerTag         = 'InputTag("TriggerResults","","HLT")' if isMC==False else 'InputTag("TriggerResults","","RECO")'   # Run Fill EB only if the HLTPaths for EB(ee) exist, in 93X MC we also have "TriggerResults","","HLT"
#hltL1GtObjectMap   = 'InputTag("hltL1GtObjectMap")' not used anywhere
L1GTobjmapTag      = 'InputTag("hltGtStage2Digis")' if isMC==False else 'InputTag("gtStage2Digis","","RECO")' # this takes the BXVector<GlobalAlgBlk> for L1 trigger info
useHLTFilter       = "True" if isMC==False else "False"  # Add to the path the request of a HLT path:  process.AlcaP0Filter.HLTPaths = 
correctHits        = 'False' # this seems to add obsolete code, keep False
globaltag          = '124X_dataRun3_Prompt_v4'  if isMC==False else '123X_mcRun2_asymptotic_v1' 
FROMDIGI           = True if isMC==False else False
if runCalibrationFromRecHits:
   FROMDIGI = False
DigiCustomization  = False   # keep this False since CMSSW_7_4_15, there is a module in CMSSW providing the bunchSpacing.  ===> NEW - 03/05/2016 - : can set it True because to run (at least) on data, that introduces --> outputfile.write("process.ecalMultiFitUncalibRecHit.algoPSet.useLumiInfoRunHeader = False\n") <-- in fillEpsilonPlot*.py file, which is needed to run without errors, but it also add another line to activate process.ecalMultiFitUncalibRecHit.algoPSet.activeBXs, so keep False for now
MULTIFIT           = True;   # Choose WEIGHTS or MULTIFIT (MULTIFIT is standard)
is50ns             = False      # If DigiCustomization and MULTIFIT is True
WEIGHTS            = False;   # Choose WEIGHTS or MULTIFIT (MULTIFIT is standard)
if(Are_pi0):                                           # Member of Recalibration Module
   esInputTag = "InputTag('hltAlCaPi0RecHitsFilterEEonlyRegional','pi0EcalRecHitsES')"
   HLTPaths='AlCa_EcalPi0E*'                        # HLT Name to ask before running the event. It can contain a *.
   if Barrel_or_Endcap == 'ONLY_ENDCAP':
      HLTPaths='AlCa_EcalPi0EE*'
   elif Barrel_or_Endcap == 'ONLY_BARREL':
      HLTPaths='AlCa_EcalPi0EB*'
   HLTResultsNameEB   = 'AlCa_EcalPi0EB'            # HLT Name to ask for into the GetHLTResults (do not use name_EB* please)
   HLTResultsNameEE   = 'AlCa_EcalPi0EE'
else:
   esInputTag = "InputTag('hltAlCaEtaRecHitsFilterEEonlyRegional','etaEcalRecHitsES')"
   HLTPaths='AlCa_EcalEtaE*' #AlCa_EcalEtaEBonly_LowPU_v1 AlCa_EcalEtaEEonly_LowPU_v1
   HLTResultsNameEB   = 'AlCa_EcalEtaEB'            # HLT Name to ask for into the GetHLTResults (do not use name_EB* please)
   HLTResultsNameEE   = 'AlCa_EcalEtaEE'
if(FROMDIGI):
   ebInputTag = 'InputTag("ecalRecHit","EcalRecHitsEB","analyzerFillEpsilon")'
   eeInputTag = 'InputTag("ecalRecHit","EcalRecHitsEE","analyzerFillEpsilon")'
   if(Are_pi0): 
      EBdigi = 'InputTag("hltAlCaPi0EBRechitsToDigis","pi0EBDigis")'
      EEdigi = 'InputTag("hltAlCaPi0EERechitsToDigis","pi0EEDigis")'
   else:
      EBdigi = 'InputTag("hltAlCaEtaEBRechitsToDigis","etaEBDigis")'
      EEdigi = 'InputTag("hltAlCaEtaEERechitsToDigis","etaEEDigis")'
else:
   if isMC:
      ebInputTag = 'InputTag("ecalRecHit","EcalRecHitsEB","RECO")'
      eeInputTag = 'InputTag("ecalRecHit","EcalRecHitsEE","RECO")'
      esInputTag = 'InputTag("ecalPreshowerRecHit","EcalRecHitsES","RECO")'
   else:
      if runCalibrationFromRecHits:
         ebInputTag = 'InputTag("ecalRecHit","EcalRecHitsEB","analyzerFillEpsilon")'
         eeInputTag = 'InputTag("ecalRecHit","EcalRecHitsEE","analyzerFillEpsilon")'
      else:
         if(Are_pi0):
            ebInputTag = 'InputTag("hltAlCaPi0EBUncalibrator","pi0EcalRecHitsEB")'
            eeInputTag = 'InputTag("hltAlCaPi0EEUncalibrator","pi0EcalRecHitsEE")'
         else:
            ebInputTag = 'InputTag("hltAlCaEtaEBUncalibrator","etaEcalRecHitsEB")'
            eeInputTag = 'InputTag("hltAlCaEtaEEUncalibrator","etaEcalRecHitsEE")'

if isMC:
   MC_Assoc = True
   MC_Assoc_DeltaR = '0.1'
   genPartInputTag = 'InputTag("genParticles","")'
   pileupInputTag  = 'InputTag("addPileupInfo","","HLT")'
else:
   #Association with GenPart
   MC_Assoc = False
   isEoverEtrue = False

if isMC and isMCV1:
   inputlist_n = 'InputList/Gun_FlatPt1to15_MultiPion_withPhotonPtFilter_pythia8.list'
   globaltag   = '93X_mc2017_realistic_v3'
