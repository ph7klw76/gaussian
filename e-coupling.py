"""
    * InFile: Contains the names of the files containing the Fock and
                overlap matrices, and molecular orbital coefficients of
                fragment A and B.

          Example:
            fock       filename
            overlap    filename
            molOrbA    filename
            molOrbB    filename
    * paramFile: Contains the parameters for the calculation including
                      the number of basis functions on fragment A and B, and
                      the sets of orbitals {m,n} on fragment A and {p,q} on
                      fragment B where {m,n} and {p,q} are contiguous sets of
                      numbers m thru n and p thru q, respectively.
            
          Example:
            nBasisFunctsA    number
            nBasisFunctsB    number
            orbitalsA        number number
            orbitalsB        number number

    * outFilePrefix: Output files Prefix that are used to produced two output files: 
                     filename.out contains all information including the overlap, interaction energy,
                    and electronic coupling. filename.t contains only the electronic coupling.
"""


# after completion of calculation, you require to create logfile.txt before it can be run#
import os
import numpy as np

def findnBasisFuncts(filename):
    filename=os.getcwd()+'\\'+filename
    read_file=open(filename)
    for line in (read_file.readlines()):
        if line.__contains__('NBasis='):
            NBasis=line.split()[1]
            NBasis=int(NBasis.strip())
    return NBasis
                            
def coupling(argv):  # Take a list of arguement such as coupling(['a',2,3.5,'d']
    inFile = argv[1]
    paramFile = argv[2]
    outFilePrefix = argv[3]
    
    # open input file,parameter files
    inFile=os.getcwd()+'\\'+inFile    ## for linux it is '/'
    paramFile=os.getcwd()+'\\'+paramFile ## for linux it is '/'
    outFile=os.getcwd()+'\\'+outFilePrefix + '.out'  
    outFile2=os.getcwd()+'\\'+outFilePrefix + '.t'

    fIn = open(inFile,'r')
    fPar = open(paramFile,'r')
    # read input file for different filenames required
    for i, line in enumerate(fIn):
        print(i, line)
        if (i==1):
            fockFile = line.strip()
        if (i==0):
            overlapFile = line.strip()
        if (i==2):
            molOrbFileA = line.strip()
        if (i==3):
            molOrbFileB = line.strip()
    fIn.close()
    # open different filenames required
    fockFile=os.getcwd()+'\\'+fockFile ## for linux it is '/'
    fFock = open(fockFile,'r')
    overlapFile=os.getcwd()+'\\'+overlapFile
    fOverlap = open(overlapFile,'r')
    molOrbFileA=os.getcwd()+'\\'+molOrbFileA
    fOrb = open(molOrbFileA,'r')
    # read parameter file
    for i, line in enumerate(fPar):
        if (i==0):
            NumeroOrbital1=line.strip('NumeroOrbital1=')
            NumeroOrbital1=NumeroOrbital1.split()   # assume two numbers begin <end!!!
            orbitalsA_begin=int(NumeroOrbital1[0])
            orbitalsA_end=int(NumeroOrbital1[1])
        if (i==1):
            NumeroOrbital2=line.strip('NumeroOrbital2=')
            NumeroOrbital2=NumeroOrbital2.split()
            orbitalsB_begin=int(NumeroOrbital2[0])
            orbitalsB_end=int(NumeroOrbital2[1])
        if (i==2):     # can be simplifed by looking at long file
            FilenBasisFunctsA = line.strip()
            nBasisFunctsA=findnBasisFuncts(FilenBasisFunctsA)
        if (i==3):
            FilenBasisFunctsB = line.strip()
            nBasisFunctsB=findnBasisFuncts(FilenBasisFunctsB)
    fPar.close()

    # calculate no. of elements in overlap/Fock matrix
    nA = nBasisFunctsA
    nB = nBasisFunctsB
    nAB = nA + nB
    nMatrixElems = int(((nAB)*(nAB) + nAB)/2)
    print("No. of elements in overlap/Fock matrix =", nMatrixElems)

    fockNumel = []
    lineCount = 0
    # read Fock matrix file
    for line in fFock:
        lineCount += 1
        if (lineCount > 3):
            cols = line.split()
            nCols = len(cols)
            for i in range(nCols):
                fockNumel.append(float(cols[i]))
    fFock.close()

    k = -1
    # form Fock matrix by filling the bottom-diagonal elements first
    F = np.zeros([nAB,nAB]) 
    for i in range(nAB):
        for j in range(i+1):
            k = k + 1
            F[i,j] = fockNumel[k]

    # form the top-diagonal elements by symmetry
    for i in range(nAB):
        for j in range(i+1,nAB):
            F[i,j] = F[j,i]

    overlapNumel = []
    lineCount = 0
    # read overlap matrix file
    for line in fOverlap:
        lineCount += 1
        if (lineCount > 3):
            cols = line.split()
            nCols = len(cols)
            for i in range(nCols):
                overlapNumel.append(float(cols[i]))
    fOverlap.close()

    k = -1
    # form overlap matrix by filling the bottom-diagonal elements first
    O = np.zeros([nAB,nAB]) 
    for i in range(nAB):
        for j in range(i+1):
            k = k + 1
            O[i,j] = overlapNumel[k]

    # form the top-diagonal elements by symmetry
    for i in range(nAB):
        for j in range(i+1,nAB):
            O[i,j] = O[j,i]


    lenOfCoeff = 15  #?? danger
    nCoeffsPerLine = 5   #??? danger
    
    orbCount = 0
    orbFlag = 0
    nOrbLines = nBasisFunctsA/nCoeffsPerLine + 1
    orbCoeffsA = {}
    # read file containing MOs of fragment A
    line = fOrb.readline()    # read and ignore first line of file
    while 1:
        line = fOrb.readline()
        if not line: break

        if (orbFlag > 0):
            for i in range(nCoeffsPerLine):
                coeff = line[lenOfCoeff*i:lenOfCoeff*(i+1)]
                if (coeff != "") and (coeff != "\n"):
                    if not line.__contains__('Alpha'):
                        base = float(coeff.split('D')[0])
                        power = int(coeff.split('D')[1])
                        coeff = "%fe%d" % (base,power)
                        orbCoeffsA[orbCount].append(float(coeff))
            orbFlag += 1
            if (orbFlag == nOrbLines+1):
                orbFlag = 0

        cols = line.split()
        if (len(cols) > 1):
            if (cols[1] == 'Alpha'):
                orbCoeffsA[int(cols[0])] = []
                orbCount += 1
                orbFlag = 1
                
                
    # open file containing molecular orbitals of fragment B
    molOrbFileB=os.getcwd()+'\\'+molOrbFileB
    fOrb = open(molOrbFileB,'r')
    
    orbCount = 0
    orbFlag = 0
    nOrbLines = nBasisFunctsB/nCoeffsPerLine + 1
    orbCoeffsB = {}
    # read file containing MOs of fragment B
    line = fOrb.readline()    # read and ignore first line of file
    while 1:
        line = fOrb.readline()
        if not line: break

        if (orbFlag > 0):
            for i in range(nCoeffsPerLine):
                coeff = line[lenOfCoeff*i:lenOfCoeff*(i+1)]
                if (coeff != "") and (coeff != "\n"):
                    if not line.__contains__('Alpha'):
                        base = float(coeff.split('D')[0])
                        power = int(coeff.split('D')[1])
                        coeff = "%fe%d" % (base,power)
                        orbCoeffsB[orbCount].append(float(coeff))
            orbFlag += 1
            if (orbFlag == nOrbLines+1):
                orbFlag = 0

        cols = line.split()
        if (len(cols) > 1):
            if (cols[1] == 'Alpha'):
                orbCoeffsB[int(cols[0])] = []
                orbCount += 1
                orbFlag = 1
                
    # Compute coupling between orbital orbA on fragment A and orbital orbB
    # on fragment B for orbA in {m,...,n} and orbB in {p,...,q} as defined
    # in the parameter file

    HARTREE2EV = 27.2114
    
    
    with open(outFile, 'w') as fOut:
        with open(outFile2,'w') as fOut2:
            for orbA in range(orbitalsA_begin,orbitalsA_end+1):
                for orbB in range(orbitalsB_begin,orbitalsB_end+1):
        
                    Saa = 0.0
                    Eaa = 0.0
                    for i in range(nBasisFunctsA):
                        for j in range(nBasisFunctsA):
                            Saa += orbCoeffsA[orbA][i]*O[i,j]*orbCoeffsA[orbA][j]
                            Eaa += orbCoeffsA[orbA][i]*F[i,j]*orbCoeffsA[orbA][j]
                    Eaaev = Eaa*HARTREE2EV
        
                    Sbb = 0.0
                    Ebb = 0.0
                    for i in range(nBasisFunctsB):
                        for j in range(nBasisFunctsB):
                            p = i + nBasisFunctsA
                            q = j + nBasisFunctsA
        #                    print(i, orbB, orbitalsB_end)
        #                    print(i, orbCoeffsB[orbB][i])
                            Sbb += orbCoeffsB[orbB][i]*O[p,q]*orbCoeffsB[orbB][j]
                            Ebb += orbCoeffsB[orbB][i]*F[p,q]*orbCoeffsB[orbB][j]
                    Ebbev = Ebb*HARTREE2EV
        
                    Sab = 0.0
                    Eab = 0.0
                    for i in range(nBasisFunctsA):
                        for j in range(nBasisFunctsB):
                            p = j + nBasisFunctsA
                            Sab += orbCoeffsA[orbA][i]*O[p,i]*orbCoeffsB[orbB][j]
                            Eab += orbCoeffsA[orbA][i]*F[p,i]*orbCoeffsB[orbB][j]
                    Eabev = Eab*HARTREE2EV
        
                    tABev = (Eabev - ((Eaaev+Ebbev)*Sab/2))/(1-Sab*Sab)
                    print("  ****************************************", file=fOut)
                    print('\n') 
                    print("Interaction btw MO", orbA,"on fragment A and MO", orbB, "on fragment B", file=fOut)
                    print('\n') 
                    print("S(A,A) =",Saa, "E(A,A) =",Eaa,"au","(",Eaaev,"eV)", file=fOut)
                    print("S(B,B) =",Sbb,  "E(B,B) =", Ebb, "au","(",Ebbev, "eV)", file=fOut)
                    print('\n')
                    print("S(A,B) =",Sab, "E(A,B) =",Eab,"au","(",Eabev,"eV)", file=fOut)
                    print('\n')
                    print("t(",orbA,",",orbB,")=",tABev,"eV", file=fOut)
                    print('\n')
                    print('\n')
                    print("t(",orbA,",",orbB,")=",tABev,"eV", file=fOut2)
    fOut.close()
    fOut2.close()


                
coupling(['a','data.in','logfile.txt','d']) # 'dimensionOM-n1n2plusieursOM.in' filename
