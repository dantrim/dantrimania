from scipy.special import betainc
from scipy.stats import norm
import numpy as np

def pvalue_to_z( p ) :
    """ Follows the RooStats::PValueToSignificance method
    https://root.cern.ch/doc/v606/RooStatsUtils_8h_source.html
    """

    return -1.0 * norm.ppf(p)

def binomial_exp_z(s, b, rel_unc_b) :
    """ Follows the significance Z-value calculation for
    RooStats::NumberCountingUtils::BinomialExpZ(S, B, DeltaB)
    https://root.cern.ch/root/html526/src/RooStats__NumberCountingUtils.cxx.html
    """

    if b == 0 :
        return -5

    if s == 0 :
        return -5

    if s / b < 1e-3 :
        return -5

    total_assumed = s + b
    tau = 1.0 / b / ( rel_unc_b * rel_unc_b )
    auxiliary = b * tau

    return pvalue_to_z( betainc( total_assumed, auxiliary + 1, 1.0 / (1.0 + tau) ) )

def binomial_obs_z(obs, b, rel_unc_b) :
    """ Follows the significance Z-value calculation for
    RooStats::NumberCountingUtils::BinomialObsZ
    https://root.cern.ch/root/html526/src/RooStats__NumberCountingUtils.cxx.html
    """

    if b == 0 :
        return -5

    if s == 0 :
        return -5

    tau = 1. / b / ( rel_unc_b * rel_unc_b )
    auxiliary = b * tau
    return pvalue_to_z( betainc( obs, auxiliary + 1, 1.0 / (1.0 + tau) ) )
    
