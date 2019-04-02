# ********************************************************************************
#
#		Abaqus Standard 2016 Pre-Processing Script
#
#		Reads an ABAQUS output (.odb) database and calculates the stent-to-artery 
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
surf_area = [line for line in paramsFile]
surf_area = eval(surf_area[0])
#
# Define (crimped) stent parameters
outer_rad = 0.9
stent_length = 5
#
SAR = surf_area / (2 * math.pi * outer_rad * stent_length) * 100
print 'STENT-TO-ARTERY RATIO = ', SAR
#
# ********************************************************************************
# Output
# ********************************************************************************
#
# Write to text file
paramsFile = open('output_sar.txt','w')
paramsFile.write(str(SAR))
paramsFile.close()
#
# ********************************************************************************