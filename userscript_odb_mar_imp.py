# ********************************************************************************
#
#		ABAQUS/Explicit (6.14) Post-Processing Script
#
#		Reads an ABAQUS output (.odb) database and calculates the metal-to-artery 
# 		ratio of parametric stent geometries
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
paramsFile = open('surfaceAreaOuter.txt','r')
sar = [line for line in paramsFile]
sar = eval(sar[0])
#
# Define (crimped) stent parameters
outer_rad = 0.9
stent_length = 5
#
MAR = sar / (2 * math.pi * outer_rad * stent_length) * 100
print 'METAL-TO-ARTERY RATIO = ', MAR
#
# ********************************************************************************
# Output
# ********************************************************************************
#
# Write to text file
paramsFile = open('output_mar.txt','w')
paramsFile.write(str(MAR))
paramsFile.close()
#
# ********************************************************************************