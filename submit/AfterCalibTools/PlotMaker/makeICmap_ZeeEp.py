import csv, os
import pandas as pd
import itertools

# intercalibration method
intercalib_method = 'Zee'
year = '2022'
eras = 'BE'

# INPUT
# Ecal ICs from end-of-Run2 global tag
#input_txt_file = '/afs/cern.ch/work/c/camendol/public/ecal/ICs/2022/EcalIntercalibConstants_UL_Run1_Run2_v3_325308.dat' 
#IC_source = 'global_tag'
# Zee ICs with IC(prompt_2022) from global-tag
#input_txt_file = '/afs/cern.ch/user/c/camendol/public/xChiaraB/ic354780.txt'
#input_txt_file = '/afs/cern.ch/user/c/camendol/public/xChiaraB/ic356580.txt'
#input_txt_file = '/afs/cern.ch/user/c/camendol/public/xChiaraB/ic357059.txt'
#input_txt_file = '/afs/cern.ch/user/c/camendol/public/xChiaraB/ic357440.txt'
input_txt_file = '/afs/cern.ch/user/c/camendol/public/xChiaraB/ic357704.txt'
IC_source = 'fullEcalIC'
# absolute Zee ICs after 1st harness correction * etascale 
#input_txt_file = '/afs/cern.ch/work/c/camendol/public/ecal/ICs/2022/data-ecalelf-09-01.ics_etascale.354780-356578.dat'
#IC_source = 'hnsEtascale'


output_csv_file = (os.path.basename(input_txt_file).split('/')[-1]).replace('.txt', '.csv').replace('.dat','.csv')
since_run = output_csv_file.replace("ic", "").replace(".csv", "")
#since_run = '354780'
IC_outdir = './ICs_ZeeEp_{y}/'.format(y=year)
if not os.path.isdir(IC_outdir) : os.mkdir(IC_outdir)
output_csv_file = IC_outdir+IC_source+'_'+output_csv_file

if os.path.exists(input_txt_file):
    print(' [INPUT] reading ICs from ' + input_txt_file)
else :
    print(' [ERROR] cannot open input file ' + input_txt_file)

# convert IC_input.txt --> IC_input .csv
if not os.path.exists(output_csv_file):
    with open(input_txt_file, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(" ") for line in stripped if line)
        with open(output_csv_file, 'w') as out_file:
            writer = csv.writer(out_file, delimiter=',')
            writer.writerow(('ieta_', 'iphi_', 'iz_', 'coeff_'))
            writer.writerows(lines)
    out_file.close()
    in_file.close()

if os.path.exists(output_csv_file):
    print(' [OUTPUT] output .csv saved in ' + output_csv_file)
else : 
    print(' [ERROR] I can\'t find the output file ' + input_txt_file)


# output
eosDir = '/eos/user/c/cbasile/www/CalibPi0_Run3/AlCaP0_2022BE_TestCalib_iter8to10/iter_2/2DMaps/ICmaps/{method}/'.format(method=intercalib_method)
if not os.path.isdir(eosDir) : 
    os.mkdir(eosDir)
    os.system("cp ~/public/index.php " + eosDir)
# lounch the script
run_cmd = "root -l -b -q 'makeICmap_ZeeEp.C(\"{input}\", \"{payload}\",\"{source}\",\"{tree_out}\",\"{eos_out}\")'".format(input=output_csv_file,  payload=since_run, source =IC_source ,tree_out = IC_outdir, eos_out=eosDir)

#run_cmd = "root -l -b -q 'makeICmap_ZeeEp.C'"
intercalib_method = intercalib_method+'_'+IC_source+'_'+since_run
hadd_cmd = "hadd -f {dir}/calibMap_{method}.root {dir}/calibMap_{method}_EB.root {dir}/calibMap_{method}_EE.root {dir}/h_calibMap_{method}.root".format(dir = IC_outdir,method = intercalib_method)
rm_cmd = "rm {dir}/calibMap_{method}_EB.root {dir}/calibMap_{method}_EE.root {dir}/h_calibMap_{method}.root".format(dir = IC_outdir,method = intercalib_method)

print "-"*30
print(run_cmd)
os.system(run_cmd)
print(hadd_cmd)
os.system(hadd_cmd)
os.system(rm_cmd)
