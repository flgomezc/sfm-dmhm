# Last modification: 2016-feb-10 - Bogota

# OD1 Willott
# OD2 Bouwens
# OD3 Finkelstein


from numpy import *

###########################################################################
# Willott
OD1 = [array([[ -2.25000000e+01,  -2.20000000e+01,  -2.15000000e+01,
          -2.10000000e+01,  -2.05000000e+01],
        [  2.66000000e-08,   2.18000000e-06,   1.45000000e-05,
           1.29000000e-04,   2.30000000e-04],
        [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00],
        [  2.50000000e-01,   2.50000000e-01,   2.50000000e-01,
           2.50000000e-01,   2.50000000e-01]]),
 [-22.75, -22.25, -21.75, -21.25, -20.75, -20.25],
 array([ 0.46679579,  0.39893724,  0.70197551,  0.26178501,  0.39138096]),
 'Willott']

###########################################################################
# Bouwens
OD2 = [array([[ -2.25200000e+01,  -2.20200000e+01,  -2.15200000e+01,
          -2.10200000e+01,  -2.05200000e+01,  -2.00200000e+01,
          -1.95200000e+01],
        [  2.00000000e-06,   1.10000000e-05,   2.90000000e-05,
           6.00000000e-05,   1.46000000e-04,   2.96000000e-04,
           6.11000000e-04],
        [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00],
        [  2.50000000e-01,   2.50000000e-01,   2.50000000e-01,
           2.50000000e-01,   2.50000000e-01,   2.50000000e-01,
           2.50000000e-01]]),
 [-22.7, -22.27, -21.77, -21.27, -20.77, -20.27, -19.77, -19.27],
 array([ 0.30103   ,  0.16549661,  0.12299121,  0.08804563,  0.0689908 ,
         0.06654033,  0.05791511]),
 'Bouwens']

HIST2_bins=[-22.70,-22.27,-21.77,-21.27,-20.77,-20.27,-19.77,-19.27]
###########################################################################
# Finkelstein et al - 2014

OD3 = [array([[ -2.20000000e+01,  -2.15000000e+01,  -2.10000000e+01,
          -2.05000000e+01,  -2.00000000e+01,  -1.95000000e+01],
        [  9.10000000e-06,   3.38000000e-05,   7.03000000e-05,
           1.91000000e-04,   3.97000000e-04,   5.85800000e-04],
        [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
        [  2.50000000e-01,   2.50000000e-01,   2.50000000e-01,
           2.50000000e-01,   2.50000000e-01,   2.50000000e-01]]),
 [-22.25, -21.75, -21.25, -20.75, -20.25, -19.75, -19.25],
 array([ 0.22712919,  0.1216416 ,  0.08513086,  0.05434246,  0.04100839,
         0.03554075]),
 'Finkelstein']

HIST3_bins=[-22.25,-21.75,-21.25,-20.75,-20.25,-19.75,-19.25]

