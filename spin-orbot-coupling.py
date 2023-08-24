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

                                        
