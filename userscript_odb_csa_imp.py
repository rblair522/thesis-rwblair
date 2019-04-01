# ********************************************************************************
#
#		ABAQUS/Explicit (6.14) Post-Processing Script
#
#		Reads an ABAQUS output (.odb) database and calculates the recoil of
# 		parametric stent geometries
#
#		Author: Ross Blair
# 		Date:	18/02/17
#
# ********************************************************************************
#
from abaqusConstants import *
import odbAccess
from odbAccess import *
import __main__
import operator
import sys
import math
import csv
import numpy as np
#
# ********************************************************************************
# Output
# ********************************************************************************
#
# Open .odb file and define output
odb = openOdb('RECOIL.odb',readOnly=True)
step = odb.steps['RECOIL-2']
odbSet = odb.rootAssembly.\
instances['MULTILINK-STENT-1'].nodeSets['INNER NODES']
coordSys = odb.rootAssembly.DatumCsysByThreePoints(name='REFCSYS',
coordSysType=CYLINDRICAL, origin=(0,0,0),
point1=(0.0, 0.0, -1.0), point2=(0.0, 1.0, 0.0) )
#
# Field output post-recoil
lastFrame = step.frames[-1]
displacement=lastFrame.fieldOutputs['COORD']
cylindricalDisp = displacement.getTransformedField(datumCsys=coordSys)
radialDisp = cylindricalDisp.getSubset(region=odbSet)
radialValues = radialDisp.values
# for v in radialValues:
 	# print v.data[0]
radialOutput = [v.data[0] for v in radialValues]
recoilRadiusAve = sum(radialOutput)/len(radialOutput)
# print 'recoilRadiusAve = ', recoilRadiusAve
#
CSA = fabs(math.pi * recoilRadiusAve ** 2)
print 'CROSS-SECTIONAL AREA = ', CSA
#
# ********************************************************************************
# Output
# ********************************************************************************
#
# Write to text file
paramsFile = open('recoil_radius.txt','w')
paramsFile.write(str(recoilRadiusAve))
paramsFile.close()
#
# Write to text file
paramsFile = open('output_csa.txt','w')
paramsFile.write(str(CSA))
paramsFile.close()
odb.close()
#
# ********************************************************************************