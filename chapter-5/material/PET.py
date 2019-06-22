# ********************************************************************************
#
#		Abaqus Standard 2016 Pre-Processing Script
#
#		Generates an elastic-plastic constitutive model representative of PET
#		poly(ethylene terephthalate) (PET)
#
#		Author: Ross Blair
# 		Date:	07/12/17
#
# ********************************************************************************
#
# PET
m = mdb.models['Model-1']
m.Material(name='PET')
mat = mdb.models['Model-1'].materials['PET']
mat.Density(table=((1.38e-09, ), ))
mat.Elastic(table=((2500.0, 0.4), ))
#
# ********************************************************************************
