# ********************************************************************************
#
#		ABAQUS/Explicit (6.14) Post-Processing Script
#
#		Reads an ABAQUS output (.odb) database and calculates the radial stiffness 
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
import numpy.linalg as la
#
# ********************************************************************************
# Output
# ********************************************************************************
#
# Open .odb file and define output
odb = openOdb('STIFFNESS.odb',readOnly=True)
step = odb.steps['CRIMP-2']
numFrames = len(step.frames)
coordSys = odb.rootAssembly.DatumCsysByThreePoints(name='REFCSYS',
coordSysType=CYLINDRICAL, origin=(0,0,0),
point1=(0.0, 0.0, 1.0), point2=(0.0, 1.0, 0.0) )
instanceNames = ['CRIMP TOOL-1', 'CRIMP TOOL-1-rad-2',
'CRIMP TOOL-1-rad-3', 'CRIMP TOOL-1-rad-4', 
'CRIMP TOOL-1-rad-5', 'CRIMP TOOL-1-rad-6', 
'CRIMP TOOL-1-rad-7', 'CRIMP TOOL-1-rad-8']
#
# RF output for all crimp tools
force = []
forceVector = []
for word in instanceNames:
	odbSet = odb.rootAssembly.instances[word].nodeSets['RP']
	for i in range(numFrames):
		stepFrame = step.frames[i]
		stepforce = stepFrame.fieldOutputs['RF']
		cylindricalForce = stepforce.getTransformedField(datumCsys=coordSys)
		radialForce = cylindricalForce.getSubset(region=odbSet)
		radialForceValues = radialForce.values
		radialForceOutput = [v.data[0] for v in radialForceValues]
		radialForceOutput = fabs(radialForceOutput[0])
		force.append(radialForceOutput)
forceVector.append(force)
#
# Sum of RF output for all frames
forceVector = forceVector[0]
forceVectorLength = len(forceVector)
RFSUM = []
for i in range(numFrames):
	RFOutput = sum(forceVector[i:forceVectorLength:numFrames])
	RFSUM.append(RFOutput)
#
odbSet = odb.rootAssembly.nodeSets['INNER NODES ASSY']
#
# Calculate diameter at initial crimp step
firstFrame = step.frames[0]
displacement=firstFrame.fieldOutputs['COORD']
cylindricalDisp = displacement.getTransformedField(datumCsys=coordSys)
radialDisp = cylindricalDisp.getSubset(region=odbSet)
radialValues = radialDisp.values
radialOutput = [v.data[0] for v in radialValues]
initialRadiusAve = sum(radialOutput)/len(radialOutput)
#
# Calculate diameter reduction during each crimp step
crimpRadiusAveOverall = []
for i in range(numFrames):
	currentFrame = step.frames[i]
	displacement=currentFrame.fieldOutputs['COORD']
	cylindricalDisp = displacement.getTransformedField(datumCsys=coordSys)
	radialDisp = cylindricalDisp.getSubset(region=odbSet)
	radialValues = radialDisp.values
	radialOutput = [v.data[0] for v in radialValues]
	crimpRadiusAve = sum(radialOutput)/len(radialOutput)
	crimpRadiusAveOverall.append(crimpRadiusAve)
#
CRIMP = np.divide(
np.subtract(crimpRadiusAveOverall, initialRadiusAve), initialRadiusAve)*100
CRIMP = np.fabs(CRIMP)
#
# Interpolate to calculate RFSUM at 10% CRIMP
RFSUM10 = np.interp(10.0, CRIMP, RFSUM)
#
# Read in outer surface area of stent
paramsFile = open('surfaceAreaOuter.txt','r')
surfaceAreaOuter = [line for line in paramsFile][0]
surfaceAreaOuter = float(surfaceAreaOuter)
#
# Calculate pressure required to crimp stent
RS = (RFSUM10/surfaceAreaOuter*10**6)/8
#
# ********************************************************************************
# Output
# ********************************************************************************
#
# Write to text file
paramsFile = open('output_rs.txt','w')
paramsFile.write(str(RS))
paramsFile.close()
odb.close()
#
# ********************************************************************************