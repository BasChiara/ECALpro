#!/bin/bash

eosPath="/eos/cms/store/group/dpg_ecal/comm_ecal/pi0/"
dirName="AlCaP0_2023BCD_TestCalib_iter4to10"                            # dirname (see CalibCode/submit/parameters.py)  
iter_number="6"                                                          # number n of iterations (iter_0 to iter_{n-1})
tagName="${dirName}_"                           # TagName (see CalibCode/submit/parameters.py)  

# will copy output here, if directory exists
wwwTargetDir="/eos/user/c/cbasile/www/CalibPi0_Run3/${dirName}/TestConvergence/"               

nJump=1
# leave extension as "noExtension" in you don't need to add additional steps that start from the one above
# format is newDirName_ext1,newIterNumber_ext1,newTagName_ext1:newDirName_ext2,newIterNumber_ext2,newTagName_ext2 and so on (different extensions separated by : )
extension="noExtension"
extensionDirName="AlCaP0_2023BCD_TestCalib_iter4to10"
#extension="${extensionDirName},6,${extensionDirName}_"
detectorToSkip="no"   # detectorToSkip = "no" to skip nothing, "EB" to skip EB, "EE" to skip EE
saveHistograms=1  # = 0 to skip drawing histograms (will only save final convergence graph, saving space). Any value different from 0 is equivalent to true

for option in "$@";
do
    if [ "$option" = "-noEB" ]; then
        detectorToSkip="EB"
    elif [ "$option" = "-noEE" ]; then
        detectorToSkip="EE"
    fi
    if [ "$option" = "-noext" ]; then
	extension="noExtension"
    fi
    if [ "$option" = "-nohist" ]; then
	saveHistograms=0
    fi
done


if [ "${extension}" != "noExtension" ]
then
    echo "Extension added: will store plots in --> ${wwwTargetDir} (if it exists)"
    wwwTargetDir=${wwwTargetDir}extension
fi


#compile Convergence.C
g++ -Wall -pedantic -lm -o Convergence Convergence.C `$ROOTSYS/bin/root-config --cflags --libs` 

if [ $? -ne 0 ]
then
    echo "Compiling Convergence.C : failed!"
    return 0
fi
echo "Compiling Convergence.C : success :)"

echo "Now runnning Convergence.C"
./Convergence $eosPath $dirName $iter_number $tagName $nJump $extension $detectorToSkip $saveHistograms

if [ $? -ne 0 ]
then
    echo "An error occurred! Exit"
    return 0
fi
# copy output to wwwTargetDir if it exists and remove local directory, otherwise just keep in local
test -d ${wwwTargetDir}/ && cp ./plot_${dirName}/* ${wwwTargetDir}/ && rm -r ./plot_${dirName}/ 
echo " move the output from ./plot_${dirName}/ to ${wwwTargetDir}/"
echo " remove ./plot_${dirName}/" 


echo "THE END!"
