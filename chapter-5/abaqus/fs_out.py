# ********************************************************************************
#
#		Abaqus Standard 2016 Pre-Processing Script
#
#		Reads an ABAQUS output (.odb) database and calculates the foreshortening 
# 		of parametric stent geometries
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
# Define output
odb = openOdb('RECOIL.odb',readOnly=True)
coordSys = odb.rootAssembly.DatumCsysByThreePoints(name='REFCSYS', 
coordSysType=CARTESIAN, 
origin=(0,0,0), point1=(1.0, 0.0, 0.0), point2=(0.0, 1.0, 0.0) )
#
step = odb.steps['INFLATE']
#
# Average x coordinates of three end nodes on stent LHS pre-inflation
odbSetL = odb.rootAssembly.instances['MULTILINK-STENT-1'].nodeSets['END NODES L PLANAR']
firstFrame = step.frames[0]
displacement = firstFrame.fieldOutputs['COORD']
cartesianDisp = displacement.getTransformedField(datumCsys=coordSys)
positionL = cartesianDisp.getSubset(region=odbSetL)
positionIVL = positionL.values
positionIVLArray = [v.data for v in positionIVL]
pil1 = positionIVLArray[0][0]
pil2 = positionIVLArray[1][0]
pil3 = positionIVLArray[2][0]
pilave = np.average((pil1, pil2, pil3))
#
# Average x coordinates of three end nodes on stent RHS pre-inflation
odbSetR = odb.rootAssembly.instances['MULTILINK-STENT-1'].nodeSets['END NODES R PLANAR']
firstFrame = step.frames[0]
displacement = firstFrame.fieldOutputs['COORD']
cartesianDisp = displacement.getTransformedField(datumCsys=coordSys)
positionR = cartesianDisp.getSubset(region=odbSetR)
positionIVR = positionR.values
positionIVRArray = [v.data for v in positionIVR]
pir1 = positionIVRArray[0][0]
pir2 = positionIVRArray[1][0]
pir3 = positionIVRArray[2][0]
pirave = np.average((pir1, pir2, pir3))
#
step = odb.steps['RECOIL-2']
#
# Average x coordinates of three end nodes on stent LHS post-inflation
odbSetL = odb.rootAssembly.instances['MULTILINK-STENT-1'].nodeSets['END NODES L PLANAR']
lastFrame = step.frames[-1]
displacement = lastFrame.fieldOutputs['COORD']
cartesianDisp = displacement.getTransformedField(datumCsys=coordSys)
positionL = cartesianDisp.getSubset(region=odbSetL)
positionFVL = positionL.values
positionFVLArray = [v.data for v in positionFVL]
pfl1 = positionFVLArray[0][0]
pfl2 = positionFVLArray[1][0]
pfl3 = positionFVLArray[2][0]
pflave = np.average((pfl1, pfl2, pfl3))
#
# Average x coordinates of three end nodes on stent RHS post-inflation
odbSetR = odb.rootAssembly.instances['MULTILINK-STENT-1'].nodeSets['END NODES R PLANAR']
lastFrame = step.frames[-1]
displacement = lastFrame.fieldOutputs['COORD']
cartesianDisp = displacement.getTransformedField(datumCsys=coordSys)
positionR = cartesianDisp.getSubset(region=odbSetR)
positionFVR = positionR.values
positionFVRArray = [v.data for v in positionFVR]
pfr1 = positionFVRArray[1][0]
pfr2 = positionFVRArray[1][0]
pfr3 = positionFVRArray[2][0]
pfrave = np.average((pfr1, pfr2, pfr3))
#
initialLength = pilave - pirave
finalLength = pflave - pfrave
#
FORESHORTENING = (finalLength - initialLength) / initialLength * 100.0
FS = fabs(FORESHORTENING)
print 'FORESHORTENING = ', FS
#
# ********************************************************************************
# Output
# ********************************************************************************
#
# Axial edge label for rigid plate orientation
paramsFile = open('expandedstentlength.txt','w')
paramsFile.write(str(finalLength))
paramsFile.close()
#
# Write to text file
paramsFile = open('output_fs.txt','w')
paramsFile.write(str(FS))
paramsFile.close()
odb.close()
#
# ********************************************************************************