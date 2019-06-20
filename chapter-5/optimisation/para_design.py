    
# ********************************************************************************
#
#		Parametric Analysis Script
#
#		Geometry, material and Abaqus files are modified for each entry of a 40 point 
#		Latin Hypercube (LHC) sampling plan.
#
#		Author: Ross Blair
# 		Date:	09/10/18
#
# ********************************************************************************
#
import csv
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import os
import shutil
from distutils.dir_util import copy_tree
from pyKriging.samplingplan import samplingplan
from pathlib import Path
from pyDOE import *
#
# ********************************************************************************
# LHC inputs
# ********************************************************************************
#
# Design parameters and bounds (ar, w, t, l)
params_base = np.array([1.0, 0.00015, 0.00015, 0.00100])
params_lb = np.array([1.0, 0.00010, 0.00010, 0.00090])
params_ub = np.array([2.3, 0.00020, 0.00020, 0.00120])
#
# LHC sampling plan
params_no = len(params_base)
sp = samplingplan(params_no)
lhc_us = sp.optimallhc(40)
lhc_ps = np.empty((0, params_no))
for i in range(len(lhc_us)):
	ar = (params_ub[0] - params_lb[0]) * lhc_us[i,0] + params_lb[0]
	w = (params_ub[1] - params_lb[1]) * lhc_us[i,1] + params_lb[1]
	t = (params_ub[2] - params_lb[2]) * lhc_us[i,2] + params_lb[2]
	l = (params_ub[3] - params_lb[3]) * lhc_us[i,3] + params_lb[3]
	params_group = [ar,w,t,l]
	lhc_ps = np.append(lhc_ps, [params_group], axis=0)
design_matrix = lhc_ps
print design_matrix
#
# ********************************************************************************
# Optimisation pre-processing and function definitions
# ********************************************************************************
#
# Generate optimisation results file template
with open('results.txt', 'w') as paramsFile:
	paramsFile.write('Created by Python 27 on '
	+ dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n'+'\n')
	paramsFile.write('Column 1: ar'+'\n')
	paramsFile.write('Column 2: w'+'\n')
	paramsFile.write('Column 3: t'+'\n')
	paramsFile.write('Column 4: l'+'\n')
	paramsFile.write('Column 5: csa'+'\n')
	paramsFile.write('Column 6: fs'+'\n')
	paramsFile.write('Column 7: mar'+'\n')
	paramsFile.write('Column 8: rs'+'\n'+'\n')
#
# ********************************************************************************
# Run LHC
# ********************************************************************************
#
for i in range(len(design_matrix)):
	# Parameters
	ar = design_matrix[i][0]
	w = design_matrix[i][1]
	t = design_matrix[i][2]
	l = design_matrix[i][3]
	with open('results.txt', 'a') as paramsFile:
		paramsFile.write('{0:.3f}'.format(ar) + ',' + '{0:.6f}'.format(w) + ',' + '{0:.6f}'.format(t) + ',' + '{0:.6f}'.format(l) + ',')
	#
	# Create results folder
	new_folder = 'D:\DOE-{}'.format(i+1)
	if not os.path.exists(new_folder):
		os.makedirs(new_folder)
	#
	# SolidWorks
	os.chdir('D:\Geometry')
	os.system('del *.SAT')
	with open('geometry_params_w.txt', 'w') as paramsFile:
		paramsFile.write(str(w))
	with open('geometry_params_t.txt', 'w') as paramsFile:
		paramsFile.write(str(t))
	with open('geometry_params_l.txt', 'w') as paramsFile:
		paramsFile.write(str(l))
	os.system('os_command_sldwrks.bat')
	os.rename('D:\Geometry\Stent.SAT', '{}\Stent.SAT'.format(new_folder))
	#
	# Constitutive model
	os.chdir('D:\Material')
	with open('PLLA.py', 'r') as paramsFile:
		lines = paramsFile.readlines()
	lines[18] = 'ar = {}\n'.format(ar)
	with open('PLLA.py', 'w') as paramsFile:
		paramsFile.writelines(lines)
	shutil.copy2('D:\Material\PLLA.py', '{}\PLLA.py'.format(new_folder))
	#
	# Abaqus
	copy_tree('D:\Scripts\Implicit', '{}'.format(new_folder))
	os.chdir('D:\\')
#
# ********************************************************************************
