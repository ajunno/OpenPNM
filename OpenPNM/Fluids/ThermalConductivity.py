
"""
module ThermalConductivity
===============================================================================

"""
import OpenPNM
import scipy as sp

def constant(fluid,value=0.001,**params):
    return value

def na(fluid,**params):
    return 'n/a'

def Chung(fluid,Tc=132.64,Cv=1000,MW=0.0291,acentric=0.03,**params):
    r"""
    Uses Chung et al. model to estimate thermal conductivity for gases with low pressure(<10 bar) from first principles at conditions of interest 

    Parameters
    ----------
    Tc :  float, array_like
        Critical Temperature of the component (K)
    Cv :  float, array_like
        Heat capacity at constant volume (J/(mol.K))
    MW : float, array_like
        Molecular weight of the component (kg/mol)
    acentric : float, array_like
        Acentric factor of the component 

    """    
    R = 8.314    
    T = fluid.pore_conditions['temperature']    
    mu = fluid.pore_conditions['viscosity']
    Tr = T/Tc
    z = 2.0 + 10.5*Tr**2
    beta = 0.7862 - 0.7109*acentric + 1.3168*acentric**2
    alpha = Cv/R -3/2
    s = 1 + alpha*((0.215+0.28288*alpha-1.061*beta+0.26665*z)/(0.6366+beta*z+1.061*alpha*beta))
    k = 3.75*s*(mu)*R/(MW)

    return k

def Sato(fluid,Tc=647.096,Tb=373.15,MW=0.0181,**params):
    r"""
    Uses Sato et al. model to estimate thermal conductivity for pure liquids from first principles at conditions of interest

    Parameters
    ----------
    Tc :  float, array_like
        Critical Temperature of interest (K)
    Tb :  float, array_like
        Boiling temperature of the component (K)
    MW : float, array_like
        Molecular weight of the component (kg/mol)


    """     
    T = fluid.pore_conditions['temperature']
    Tbr = Tb/Tc
    Tr = T/Tc
    k = (1.11/((MW*1e3)**0.5))*(3+20*(1-Tr)**(2/3))/(3+20*(1-Tbr)**(2/3))
    return k