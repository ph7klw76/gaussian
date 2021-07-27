import subprocess
import time
from shutil import copyfile
import numpy as np
import math
import os


def make_sh_file(myfile):
    sh_file=str(myfile)+'.sh'
    f = open(sh_file, 'w')
    sh= open('./gaussian0.sh')
    for i, line in enumerate(sh):
        if i!=3:
            f.write(line)
        if i==3:
            line1='#SBATCH --job-name='+myfile
            line1=str(line1)
            f.write(line1)
            f.write('\n')
        if i==13:
            f.write('g09 <'+str(myfile)+'.com > '+str(myfile)+'.log')
    f.close()
    path='./'+ sh_file
    path=str(path)
    subprocess.run(['sbatch', path])


def check_run_status():
    time.sleep(60)
    read_file=open('./automation.out') # jobname
    for i, line in enumerate(read_file):
        job_id=line.split()[3]
    check_status='squeue -h -j '+ str(job_id)
    process=subprocess.run(check_status, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    while output.__contains__(job_id):
        time.sleep(10)
        process=subprocess.run(check_status, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = process.stdout 
    return True


myfilelist=['3,6-DPXZ-AD','3Cz2DMeCzBN','3Cz2DPhCzBN','4CzBN','5CzBN','6PXZ-PR','8PXZ-PRB','BP-phIDID']
for myfile in myfilelist:
    make_sh_file(myfile)
    done=check_run_status()
