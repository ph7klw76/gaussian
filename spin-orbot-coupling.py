# have attached here two files: 
#init.py (code read by pySOC during execution) 
#and 
#pobPySOC- execution script on OSAKA


#Steps to run pySOC:
#1- run TDDFT (with GAUSSIAN !!) on the molecule (for instance LS190). 
#In the com file, these indications are mandatory:
# %rwf=LS190
# %chk=LS190
# %nprocshared=32
# #p td=(50-50,nstates=10) wb97xd scrf=(solvent=toluene) def2svp 6D 10F
# GFinput # nosym iop(3/107=0033200000,3/108=0033200000)

#In the log file, If you run Gaussian16, there is nothing to do. If you run Gaussian 09, there are three lines to remove from the log file: 
# Integral buffers will be    131072 words long.
# Raffenetti 2 integral format.
# Two-electron integral symmetry is turned off.
#This is a stupid thing in pysoc:  the calculation of pySOC is crashed if the three lines are not removed. 
#In gaussian16 log file these lines are absent.

#2- Create a folder for "LS190". Copy-paste inside :
#cp LS190.log LS190/gaussian.log
#cp LS190.chk LS190/gaussian.chk
#cp LS190.rwf LS190/gaussian.rwf
#cp init.py LS190/.
#cp pobPySOC LS190/.

#The name of the log-chk-rwf files MUST be gaussian !! ... no comments !!
#This is the reason you need to create a folder for each molecule.

#3- run  pobPySOC

#module called by soc.py
#general control for spin-orbit coupling calculation

import sys
#control parameter
QM_ex_flag = False #False we do QM calculation separately
QM_code = 'gauss_tddft' # gauss_tddft or tddftb
#QM_code = 'tddftb' # gauss_tddft or tddftb
n_s = [1, 2, 3, 4, 5, 6, 7, 8, 9] #default # of excited singlets
n_t = [1, 2, 3, 4, 5, 6, 7, 8, 9] #default # of excited triplets
n_g = ['True']       #default including ground state
soc_scal = 1.0 #scaling factor for Zeff in SOC operator
cicoeff_thresh = [1.0e-5] #thresh hold for ci coeff 

# environmental variable
g09root = '/usr/local'
sys.path.append(g09root+'/g09')

##molsoc code from Sandro Giuseppe Chiodo
##with small modifications for input because only the soc
##in atomic basis is needed in the following calculation 
molsoc_path = '/usr/local/pysoc/2016/bin/molsoc0.1.exe' 

#input files

if QM_code == 'gauss_tddft':
##from Gaussian output
   qm_out = ['gaussian.log', 'gaussian.rwf']
   geom_xyz = []
   soc_key  = ['ANG', 'Zeff', 'DIP']
elif QM_code == 'tddftb':
##from TD-DFTB+ output
   qm_out = ['band.out', 'EXC.DAT', 'oversqr.dat', 'eigenvec.out', \
             'XplusY.DAT', 'SPX.DAT']
   geom_xyz = ['dty.xyz']
   soc_key  = ['ANG', 'Zeff', 'DIP', 'TDB']
dir_para_basis = '/fsnfs/users/xinggao/work/gsh/thiothymine/gtsh/test_python/tddftb/sto2gto/mio-1-1'
##input for molsoc(to be generated) 
molsoc_input = ['molsoc.inp', 'molsoc_basis']

##from Newton-X 
newton_x = ['geom', 'basis', 'control.dyn']



                                        
