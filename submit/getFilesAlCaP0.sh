#! /bin/bash

thisYear="23"   # use 16, 17, 18, 22, 23 ecc...
dayMonthYear=`date +%d_%m_%Y`
dataset="AlCaP0"
runYear="20${thisYear}"
# 2022 Golden json (era B-G)
#JsonFilter="/eos/user/c/cmsdqm/www/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json"
# 2023 Golden json (era B-D)
JsonFilter="/eos/user/c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json"
# 2023 DCSonly json
#JsonFilter="/eos/user/c/cmsdqm/www/CAF/certification/Collisions23/DCSOnly_JSONS/Collisions23_13p6TeV_eraBCD_366403_370790_DCSOnly_TkPx.json"
firstRunBrilcalc="" # can be empty, otherwise it is used to select a run range for the brilcalc command
lastRunBrilcalc="" # can be empty, otherwise it is used to select a run range for the brilcalc command

ecalproFolder="${CMSSW_BASE}/src/CalibCode/submit/"
outputdir="${ecalproFolder}InputList/"
outputfile="${dataset}_Run${runYear}${dataEra}_${dayMonthYear}.list"
fileList="${outputdir}${outputfile}"
brilcalcOutputFile="${ecalproFolder}brilcalc_${outputfile/list/txt}"

cd ${ecalproFolder}
eval `scramv1 runtime -sh`

host=`echo "$HOSTNAME"`
if [[ ${host} != *"lxplus"* ]]; then
    echo "Error! You must be on lxplus to get list of files. Do ssh -XY lxplus and work from a release."
    return 0
fi

echo "Creating list of file running dasgoclient"
eras=(A B C D E F G H I L M N O P Q R S T U V Z)
eras=(B C D ) 
echo "" > ${fileList}
for dataEra in ${eras[@]} 
do 
    echo "dasgoclient --query=\"file dataset=/${dataset}/Run${runYear}${dataEra}-v1/RAW\""
    dasgoclient -query="file dataset=/${dataset}/Run${runYear}${dataEra}-v1/RAW" >> ${fileList} 
done
echo "List created in ${fileList}"

echo ""
echo "Filtering list of files with json ${JsonFilter}"
purifyCmd="python3 Utilities/Purify_List.py ${fileList} ${JsonFilter}"
echo "${purifyCmd}"
echo "${purifyCmd}" | bash

#echo ""
#echo "Checking integrated luminosity with brilcalc"
#brilcalcCmd="brilcalc lumi -u /fb -i ${JsonFilter} --without-checkjson --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json" # normtag_PHYSICS.json 
#if [[ "X${firstRunBrilcalc}" != "X" ]]; then
#    brilcalcCmd="${brilcalcCmd} --begin ${firstRunBrilcalc}"
#fi
#if [[ "X${lastRunBrilcalc}" != "X" ]]; then
#    brilcalcCmd="${brilcalcCmd} --end ${lastRunBrilcalc}"
#fi
#echo "${brilcalcCmd}"
#echo "Will save output in file ${brilcalcOutputFile}"
#echo "${brilcalcCmd} > ${brilcalcOutputFile}" | bash

echo ""
echo "DONE!" 
echo ""
