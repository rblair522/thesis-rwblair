# ********************************************************************************
#
#		Abaqus Standard 2016 Pre-Processing Script
#
#		Generates an orthotropic elastic-plastic constitutive model representative
#		of poly(L-lactic acid) (PLLA)
#
#		Author: Ross Blair
# 		Date:	07/12/17
#
# ********************************************************************************
#
import numpy as np
#
# ********************************************************************************
# Coefficients
# ********************************************************************************
#
# Elastic coefficients
ar = 1.13625
if 1 <= ar <= 2.3:
	ar_mod = ar
elif 0 < ar <1:
	ar_mod = 1/ar
else:
	print('Check aspect ratio definition')
E1 = 3062-555*ar_mod
E2 = 2196+618*ar_mod
ys1 = 65-11*ar_mod
ys2 = 46+10*ar_mod
eb = 0.5
eb1_true = np.log(1+eb)
uts1_true = ys1*(1+eb1_true)
v1 = 0.35
v2 = v1
G1 = E1/(2*(1+v1))
G2 = 1/(1/E1+1/E2+2*v2/E2)
#
if 1 <= ar <= 2.3:
	# Circumferential
	D = np.matrix(
	[[1/E1, -v2/E2, -v1/E1, 0, 0, 0],
	[-v2/E2, 1/E2, -v2/E2, 0, 0, 0],
	[-v1/E1, -v2/E2, 1/E1, 0, 0, 0],
	[0, 0, 0, 1/G2, 0, 0],
	[0, 0, 0, 0, 1/G1, 0],
	[0, 0, 0, 0, 0, 1/G2]])
elif 0 < ar <1:
	# Axial
	D = np.matrix(
	[[1/E1, -v1/E1, -v2/E2, 0, 0, 0],
	[-v1/E1, 1/E1, -v2/E2, 0, 0, 0],
	[-v2/E2, -v2/E2, 1/E2, 0, 0, 0],
	[0, 0, 0, 1/G2, 0, 0],
	[0, 0, 0, 0, 1/G2, 0],
	[0, 0, 0, 0, 0, 1/G1]])
else:
	print('Check aspect ratio definition')
#
D = np.linalg.inv(D)
#
D1111 = D[0,0]
D1122 = D[0,1]
D2222 = D[1,1]
D1133 = D[0,2]
D2233 = D[1,2]
D3333 = D[2,2]
D1212 = D[3,3]
D1313 = D[4,4]
D2323 = D[5,5]
#
if 1 <= ar <= 2.3:
	# Circumferential stress ratio coefficients
	R11 = 1.0
	R22 = ys2/ys1
	R33 = 1.0
	R12 = 1.0
	R13 = 1.0
	R23 = 1.0
elif 0 < ar <1:
	# Axial stress ratio coefficients
	R11 = 1.0
	R22 = 1.0
	R33 = ys2/ys1
	R12 = 1.0
	R13 = 1.0
	R23 = 1.0
else:
	print('Check aspect ratio definition')
#
# ********************************************************************************
# Material model
# ********************************************************************************
#
m = mdb.models['Model-1']
m.Material(name='PLLA')
mat = m.materials['PLLA']
#
# Density
mat.Density(table=((1.2e-06, ), ))
#
# Elastic
mat.Elastic(table=((
D1111, 
D1122, 
D2222, 
D1133, 
D2233, 
D3333, 
D1212, 
D1313, 
D2323
), ), type=ORTHOTROPIC)
#
# Plastic coefficients
mat.Plastic(table=(
(ys1, 0.00000),
(uts1_true, eb-uts1_true/E1)
))
#
mat.plastic.Potential(table=((
R11,
R22,
R33,
R12,
R13,
R23), ))
#
# ********************************************************************************