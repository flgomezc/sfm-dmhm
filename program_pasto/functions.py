import numpy as np
import pylab as P
from random             import *
from constants          import *
from observational_data import *
# 2014-nov-24: MCMC modification.

def Luminosity(M,L_0,M_0,beta,gamma):
    return L_0*M*( (M/M_0)**(-beta) + (M/M_0)**gamma)**(-1)

def StarFormationRate(M,L_0,M_0,beta,gamma):
    return Luminosity(M,L_0,M_0,beta,gamma) * 1.4e-28

def Dust_Extinction():
    if ( Dust_Ext == 1):
        print "Dust Extinction ON"
    else:
        print "Dust Extinction OFF"
    #return 0

def MCMC( BoxLength, MonteCarloSteps, M, L_0, M_0, beta, gamma,MCMC_reg, *DataSets):

# Markov Chain  Monte Carlo function.
#
# This function writes MonteCarloSteps lines in the input file MCMC_reg.
# The jump-size on the parameters space is controlled by the "constants.py" file
#
# Arguments:
#     Box size (double)
#     Monte-Carlo Steps (int)
#     Mass (array)
#     4 parameters(double)
#     Output filename (string)
#     DataSets (list) This list contains the names of the observational data to be fitted.

    seed(None)
    L   = np.zeros(M.size)
    L_R = np.zeros(M.size)
    L[:] = Luminosity( M[:], L_0, M_0, beta, gamma)
    Magnitude_UV_galaxy_list = 51.82 - 2.5 * np.log10(L[:])
 
    ### Dust Extinction
    if (Dust_Ext == 1):
        Mag = Magnitude_UV_galaxy_list
        Mag[Mag< Mag0] = ( Mag[Mag< Mag0]-4.61455)/1.2587
        Magnitude_UV_galaxy_list_R = Mag

    ### Create histograms & Normalize the histograms    
    HISTO = []
    for DS in DataSets:
        aux = 1.0 * np.histogram(Magnitude_UV_galaxy_list, bins= DS[1] )[0]
        for i in range(len(aux)):
            aux[i] = aux[i]/( (DS[1][i+1] - DS[1][i] ) * BoxLength**3)
        HISTO.append(aux)
    
    ### Calcule Chi Square using number of Degrees of Freedom
    NOB = 0
    chi_sqr = 0.0
    for i in range(len(HISTO)):
        for j in range(HISTO[i].size):
            if( HISTO[i][j] != 0.0 ):
                chi_sqr = chi_sqr + 0.5*( log10(HISTO[i][j]/DataSets[i][0][1][j]) / DataSets[i][2][j])**2
                NOB = NOB + 1
    chi_sqr /= abs(NOB-4)

    MCMC_reg.write("# L_0 \t M_0 \t beta \t gamma \t chi_sqr \t Number of Bins\n")
    MCMC_reg.write(str(log10(L_0))+"\t"+
                   str(log10(M_0))+"\t"+
                   str(beta)+"\t"+
                   str(gamma)+"\t"+
                   str(chi_sqr)+"\t"+
                   str(NOB)+"\n")

    ###################################
    # Markov Chain Monte Carlo Starts #
    ###################################

    # First of all, the histogram with the original parameters must be calculated,
    # included the Xi_square deviation
    for COUNTER in range(MonteCarloSteps):
        # Then the parameters are changed in order to calculate the new histogram
        L_0R   = L_0  *10**(gauss(0.0,K0))
        M_0R   = M_0  *10**(gauss(0.0,K1))
        betaR  = beta + gauss(0.0,K2)
        gammaR = gamma+ gauss(0.0,K3)
        ### Some constraints over parameters
        while (L_0R <10**(16.75)) or (L_0R >10**(20.0)):
            L_0R   = L_0  *10**(gauss(0.0,K0))
        while (M_0R < 10.80):
            M_0R   = M_0  *10**(gauss(0.0,K1))
        while (betaR<0) or (betaR>2.0):
            betaR  = beta + gauss(0.0,K2)
        while (gammaR<0) or (gammaR>0.9):
            gammaR = gamma+ gauss(0.0,K3)

        #for i in range(M.size):
        L_R[:]    = Luminosity( M[:], L_0R, M_0R, betaR, gammaR)
        Magnitude_UV_galaxy_list_R = 51.82 - 2.5 * log10(L_R[:])

        ### Dust Extinction
        if (Dust_Ext == 1):
            Mag = Magnitude_UV_galaxy_list_R
            Mag[Mag< Mag0] = ( Mag[Mag< Mag0]-4.61455)/1.2587
            Magnitude_UV_galaxy_list_R = Mag

        ### Create histograms & Normalize the histograms    
        HISTO_R = []
        for DS in DataSets:
            aux = 1.0 * np.histogram(Magnitude_UV_galaxy_list, bins= DS[1] )[0]
            for i in range(len(aux)):
                aux[i] = aux[i]/( (DS[1][i+1] - DS[1][i] ) * BoxLength**3)
            HISTO_R.append(aux)
    
        ### Calcule Chi Square using number of Degrees of Freedom
        NOB = 0
        chi_sqr_R = 0.0
        for i in range(len(HISTO_R)):
            for j in range(HISTO_R[i].size):
                if( HISTO_R[i][j] != 0.0 ):
                    chi_sqr_R = chi_sqr_R + 0.5*( log10(HISTO_R[i][j]/DataSets[i][0][1][j]) / DataSets[i][2][j])**2
                    NOB = NOB + 1
                else:
                    chi_sqr_R = chi_sqr_R + DeltaChi
        chi_sqr_R /= abs(NOB-4)

        # If the new chi2 is better, then the new set of parameters is accepted
        Delta_chi = chi_sqr_R - chi_sqr
        if ( Delta_chi < 0):
            L_0    = L_0R
            M_0    = M_0R
            beta   = betaR
            gamma  = gammaR
            HIST1   = HIST1_R
            HIST2   = HIST2_R
            HIST3   = HIST3_R 
            chi_sqr= chi_sqr_R
            print chi_sqr, NOB , " ", COUNTER
        else:
            p = random.rand()
            #print p, exp( -Delta_chi)
            if ( p > exp( -Delta_chi) ): ## CORRECT EXPRESSION ">" ########################## 2014-oct-2014
                L_0    = L_0R
                M_0    = M_0R
                beta   = betaR
                gamma  = gammaR
                HIST1   = HIST1_R
                HIST2   = HIST2_R
                HIST3   = HIST3_R
                chi_sqr= chi_sqr_R
                print chi_sqr, NOB , "*", COUNTER
        # Storing all the good points.
        # L_0, M_0, beta, gamma, chi_sqr

############################################### 2014-oct-11
#   If chi_squ grows without limit, return to the original parameters
        if (chi_sqr > 20):
            L_0    = L_0Panic
            M_0    = M_0Panic
            beta   = betaPanic
            gamma  = gammaPanic

        MCMC_reg.write(
                            str(log10(L_0))+"\t"+
                            str(log10(M_0))+"\t"+
                            str(beta)      +"\t"+
                            str(gamma)     +"\t"+
                            str(chi_sqr)  +"\t"+
                            str(NOB)        +"\n")
        # End of the loop
    MCMC_reg.close()


def SingleHistogram( BoxLength, BOX, L_0, M_0, beta, gamma):
    histo1 = []

    STR = '../data/MD_3840_Planck1/BDM/Small_Cells/'+str(BOX)+'.dat'
    M = np.loadtxt(STR,usecols=(3,), skiprows=0)
########## Halo mass must be divided by the Hubble Parameter
    M = (1.0*M)/hpl 

    L   = np.zeros(M.size)
    L_R = np.zeros(M.size)
    L[:] = Luminosity( M[:], L_0, M_0, beta, gamma)
    Magnitude_UV_galaxy_list = 51.82 - 2.5 * np.log10(L[:])
    
    ### Dust Extinction
    if (Dust_Ext == 1):
        Mag = Magnitude_UV_galaxy_list
        Mag[Mag< Mag0] = ( Mag[Mag< Mag0]-4.61455)/1.2587
        Magnitude_UV_galaxy_list = Mag


    ### Create Histograms
    HISTO = []

    for DS in DataSets:
        aux = 1.0 * np.histogram(Magnitude_UV_galaxy_list, bins= DS[1] )[0]
        for i in range(len(aux)):
            aux[i] = aux[i]/( (DS[1][i+1] - DS[1][i] ) * BoxLength**3)
        HISTO.append(aux)
    
    NOB = 0
    chi_sqr = 0.0

    for i in range(len(HISTO)):
        for j in range(HISTO[i].size):
            if( HISTO[i][j] != 0.0 ):
                chi_sqr = chi_sqr + 0.5*( log10(HISTO[i][j]/DataSets[i][0][1][j]) / DataSets[i][2][j])**2
                NOB = NOB + 1

    chi_sqr /= abs(NOB-4)
    return HISTO

def FullHistograms():
    histo0 = []
    if ( Dust_Ext ==1):
        parameters = np.loadtxt('analysis/best_parameters_w_ext.dat',usecols=(0,1,2,3), skiprows=0); 
    else:
        parameters = np.loadtxt('analysis/best_parameters_wo_ext.dat',usecols=(0,1,2,3), skiprows=0); 

    L_0   = 10**parameters[:,0]
    M_0   = 10**parameters[:,1]
    beta  = parameters[:,2]
    gamma = parameters[:,3]
    for k in range(64):
        histo0.append( SingleHistogram( 250/hpl, k, L_0[k], M_0[k], beta[k], gamma[k]) )

    Dust_Extinction()
        
    return   histo0
