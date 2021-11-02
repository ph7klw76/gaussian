import subprocess
import shutil


def create_gaussian_py(file):
    file=str(file)
    shutil.copyfile('./gaussian-w0.py','./gaussian-w'+file+'.py')
    python_file=open('./gaussian-w'+file+'.py', 'a')
    s='myfilelist=['+'\''+file+'\''+']'
    python_file.write(s+'\n')
    python_file.write('for myfile in myfilelist:'+'\n')
    python_file.write('    w_final=gss(0.03,0.1,myfile)'+'\n')
    python_file.write('    gaussian(myfile, a=float(w_final),type=1)'+'\n')
    python_file.write('    make_sh_file(myfile)'+'\n')
    s='\'./\'+myfile+\'.log\', \'./\'+myfile+str(w_final)+\'.log\''
    python_file.write('    os.rename('+s+')'+'\n')
    python_file.close()

def create_a(file):
    file=str(file)
    a=open('./a'+file+'.sh', 'w')
    a.write('#!/bin/bash -l' +'\n')
    a.write('#SBATCH --partition=cpu-opteron' +'\n')
    a.write('#SBATCH --job-name='+file+'\n')
    a.write('#SBATCH --output=%x.out' +'\n')
    a.write('#SBATCH --error=%x.err' +'\n')
    a.write('#SBATCH --nodes=1' +'\n')
    a.write('#SBATCH --mem=32G' +'\n')
    a.write('#SBATCH --ntasks=32' +'\n')
    a.write('#SBATCH --time=7-0:00:00' +'\n')
    a.write('#SBATCH --qos=long' +'\n')
    a.write('\n')
    a.write('module load miniconda/miniconda3' +'\n')
    a.write('source activate ~/ML' +'\n')
    a.write('python '+'gaussian-w'+file+'.py'+'\n')
    a.close()
    s='./a'+file+'.sh'
    return s



myfilelist=['optDMAC-DPS-116','optDMAC-TRZ','optDPO-TXO2']    
for file in myfilelist:
    create_gaussian_py(file)
    s=create_a(file)
    subprocess.run(['sbatch', s])
