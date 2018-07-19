from numpy import *
from math import *

def coeff_correl(onset_env1, onset_env2, interval):
    (start, end) = interval
    n1 = len(onset_env1)
    n2 = len(onset_env2) #n1 et n2 peuvent etre differentes
    assert (start <= end and start >=0 and end <= n1 and end <= n2),"False interval"
    autocorr1 = 0.0 #autocorrelation de onset_env1
    autocorr2 = 0.0 #autocorrelation de onset_env2
    corr = 0.0 #correlation croisee
    for t in range(start,end):
        x = onset_env1[t]
        autocorr1 += x*x
        y = onset_env2[t]
        autocorr2 += y*y
        corr += x*y
    autocorr1/=(end-start)
    autocorr2/=(end-start)
    corr/=(end-start)
    if (autocorr1 < 10**(-10) or autocorr2 < 10**(-10)):
        return 0.0
    return corr/(sqrt(autocorr1*autocorr2))
