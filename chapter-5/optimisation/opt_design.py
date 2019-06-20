# ********************************************************************************
#
#		Optimisation Script
#
#		Seeks to find optimal stent designs based on the empirical models generated
#		from the LHC sampling plan.
#
#		Author: Ross Blair
# 		Date:	01/11/18
#
# ********************************************************************************
#
import numpy as np
from scipy.optimize import minimize
#
# ********************************************************************************
# User inputs
# ********************************************************************************
#
# Empirical model coefficients
coeff = [[-2.614,4.488e+01,-1.115e+00,-2.525e+01],
[1.603e+00,-2.661e+00,-4.730e-01,-6.917e+00],
[-5.571e-02,6.620e-03,9.627e-02,-2.497e-01],
[-2.672e-03,2.526e-02,1.530e-03,-4.223e-01],
[-7.064e-03,-6.753e-02,3.117e-03,1.103e-01],
[-3.755e-03,-6.830e-03,1.481e-03,-2.035e-03],
[7.095e-04,1.041e-03,3.258e-04,1.836e-02],
[-1.061e-03,1.163e-03,1.678e-04,-1.595e-03],
[2.558e-05,2.606e-05,-1.051e-05,-2.257e-03],
[-2.318e-05,-1.232e-05,1.589e-04,5.626e-04],
[9.834e-06,-3.570e-05,-4.189e-06,6.126e-04],
[-7.453e-02,4.846e-01,1.291e-02,2.517e+00],
[2.158e-04,1.780e-04,-1.974e-04,-9.313e-04],
[-3.600e-05,5.755e-05,1.223e-05,-2.253e-04],
[7.320e-06,2.790e-05,-1.339e-06,-1.045e-04]]
#
def rsm_models(x):
	csa = coeff[0][0] + coeff[1][0]*x[0] + coeff[2][0]*x[1] + coeff[3][0]*x[2] + coeff[4][0]*x[3] + coeff[5][0]*x[0]*x[1] + \
		  coeff[6][0]*x[0]*x[2] + coeff[7][0]*x[0]*x[3] + coeff[8][0]*x[1]*x[2] + coeff[9][0]*x[1]*x[3] + coeff[10][0]*x[2]*x[3] + \
		  coeff[11][0]*x[0]**2 + coeff[12][0]*x[1]**2 + coeff[13][0]*x[2]**2 + coeff[14][0]*x[3]**2
	fs = coeff[0][1] + coeff[1][1]*x[0] + coeff[2][1]*x[1] + coeff[3][1]*x[2] + coeff[4][1]*x[3] + coeff[5][1]*x[0]*x[1] + \
		 coeff[6][1]*x[0]*x[2] + coeff[7][1]*x[0]*x[3] + coeff[8][1]*x[1]*x[2] + coeff[9][1]*x[1]*x[3] + coeff[10][1]*x[2]*x[3] + \
		 coeff[11][1]*x[0]**2 + coeff[12][1]*x[1]**2 + coeff[13][1]*x[2]**2 + coeff[14][1]*x[3]**2
	par = coeff[0][2] + coeff[1][2]*x[0] + coeff[2][2]*x[1] + coeff[3][2]*x[2] + coeff[4][2]*x[3] + coeff[5][2]*x[0]*x[1] + \
		  coeff[6][2]*x[0]*x[2] + coeff[7][2]*x[0]*x[3] + coeff[8][2]*x[1]*x[2] + coeff[9][2]*x[1]*x[3] + coeff[10][2]*x[2]*x[3] + \
		  coeff[11][2]*x[0]**2 + coeff[12][2]*x[1]**2 + coeff[13][2]*x[2]**2 + coeff[14][2]*x[3]**2
	rs = coeff[0][3] + coeff[1][3]*x[0] + coeff[2][3]*x[1] + coeff[3][3]*x[2] + coeff[4][3]*x[3] + coeff[5][3]*x[0]*x[1] + \
		 coeff[6][3]*x[0]*x[2] + coeff[7][3]*x[0]*x[3] + coeff[8][3]*x[1]*x[2] + coeff[9][3]*x[1]*x[3] + coeff[10][3]*x[2]*x[3] + \
		 coeff[11][3]*x[0]**2 + coeff[12][3]*x[1]**2 + coeff[13][3]*x[2]**2 + coeff[14][3]*x[3]**2
	return csa, fs, par, rs
#
# Baseline inputs
x0 = [1.35,150,150,1050]
#
# Baseline outputs
x1 = [-8.04,5.72,35.32,-20.91]
#
# Optimisation algorithm
opt_method = 'SLSQP'
#
# Input parameter bounds
ar_bounds = (0.4,2.3)
w_bounds = (100,200)
t_bounds = (100,200)
l_bounds = (900,1200)
opt_bounds = (ar_bounds,w_bounds,t_bounds,l_bounds)
#
# Callback function
def print_callback(x):
	print x
#
# ********************************************************************************
# Single objective optimisation
# ********************************************************************************
#
# Objective functions
def csa_min(x):
	return rsm_models(x)[0]
def csa_max(x):
	return -rsm_models(x)[0]
def fs_min(x):
	return rsm_models(x)[1]
def fs_max(x):
	return -rsm_models(x)[1]
def par_min(x):
	return rsm_models(x)[2]
def par_max(x):
	return -rsm_models(x)[2]
def rs_min(x):
	return rsm_models(x)[3]
def rs_max(x):
	return -rsm_models(x)[3]
#
# Single objective optimisation
csa_solo_min = minimize(csa_min, x0, method=opt_method, bounds=opt_bounds)
csa_solo_max = minimize(csa_max, x0, method=opt_method, bounds=opt_bounds)
fs_solo_min = minimize(fs_min, x0, method=opt_method, bounds=opt_bounds)
fs_solo_max = minimize(fs_max, x0, method=opt_method, bounds=opt_bounds)
par_solo_min = minimize(par_min, x0, method=opt_method, bounds=opt_bounds)
par_solo_max = minimize(par_max, x0, method=opt_method, bounds=opt_bounds)
rs_solo_min = minimize(rs_min, x0, method=opt_method, bounds=opt_bounds)
rs_solo_max = minimize(rs_max, x0, method=opt_method, bounds=opt_bounds)
#
csa_solo_opt_bounds = (csa_solo_min.fun, -csa_solo_max.fun)
fs_solo_opt_bounds = (fs_solo_min.fun, -fs_solo_max.fun)
par_solo_opt_bounds = (par_solo_min.fun, -par_solo_max.fun)
rs_solo_opt_bounds = (rs_solo_min.fun, -rs_solo_max.fun)
#
# print csa_solo_opt_bounds
# print fs_solo_opt_bounds
# print par_solo_opt_bounds
# print rs_solo_opt_bounds
#
# Print results
# print csa_solo_min.x, rsm_models(csa_solo_min.x)
# print fs_solo_min.x, rsm_models(fs_solo_min.x)
# print par_solo_min.x, rsm_models(par_solo_min.x)
# print rs_solo_min.x, rsm_models(rs_solo_min.x)
#
# ********************************************************************************
# Constrained baseline optimisation
# ********************************************************************************
#
x0 = [0.4,200,200,900]
#
# Constraints
def csa_constraint(x):
	return x1[0] - rsm_models(x)[0]
def fs_constraint(x):
	return x1[1] - rsm_models(x)[1]
def par_constraint(x):
	return x1[2] - rsm_models(x)[2]
def rs_constraint(x):
	return  x1[3] - rsm_models(x)[3]
csa_const = {'type':'ineq','fun':csa_constraint}
fs_const = {'type':'ineq','fun':fs_constraint}
par_const = {'type':'ineq','fun':par_constraint}
rs_const = {'type':'ineq','fun':rs_constraint}
csa_constraints = [fs_const,par_const,rs_const]
fs_constraints = [csa_const,par_const,rs_const]
par_constraints = [csa_const,fs_const,rs_const]
rs_constraints = [csa_const,fs_const,par_const]
#
# Constrained baseline optimisation
csa_cbo_min = minimize(csa_min,x0,method=opt_method,bounds=opt_bounds,constraints=csa_constraints)
fs_cbo_min = minimize(fs_min,x0,method=opt_method,bounds=opt_bounds,constraints=fs_constraints)
par_cbo_min = minimize(par_min,x0,method=opt_method,bounds=opt_bounds,constraints=par_constraints)
rs_cbo_min = minimize(rs_min,x0,method=opt_method,bounds=opt_bounds,constraints=rs_constraints)
#
# Print results
# print csa_cbo_min.x, rsm_models(csa_cbo_min.x)
# print fs_cbo_min.x, rsm_models(fs_cbo_min.x)
# print par_cbo_min.x, rsm_models(par_cbo_min.x)
# print rs_cbo_min.x, rsm_models(rs_cbo_min.x)
#
# ********************************************************************************
# Unconstrained optimisation
# ********************************************************************************
#
# Normalised linear models
def csa_norm(x):
	csa_norm = (rsm_models(x)[0] - csa_solo_opt_bounds[0]) / (csa_solo_opt_bounds[1] - csa_solo_opt_bounds[0])
	return np.absolute(csa_norm)
def fs_norm(x):
	fs_norm = (rsm_models(x)[1] - fs_solo_opt_bounds[0]) / (fs_solo_opt_bounds[1] - fs_solo_opt_bounds[0])
	return np.absolute(fs_norm)
def par_norm(x):
	par_norm = (rsm_models(x)[2] - par_solo_opt_bounds[0]) / (par_solo_opt_bounds[1] - par_solo_opt_bounds[0])
	return np.absolute(par_norm)
def rs_norm(x):
	rs_norm = (rsm_models(x)[3] - rs_solo_opt_bounds[0]) / (rs_solo_opt_bounds[1] - rs_solo_opt_bounds[0])
	return np.absolute(rs_norm)
#
# Objective function
def uo_obj_fun(x):
	return par_norm(x) + rs_norm(x)
#
# Unconstrained optimisation
uo_opt = minimize(uo_obj_fun,x0,method=opt_method,bounds=opt_bounds)
#
# Print results
# print uo_opt.x, rsm_models(uo_opt.x)
#
# ********************************************************************************
# User-constrained optimisation
# ********************************************************************************
#
# Constraints
def rs_constraint(x):
	return -40 - rsm_models(x)[3]
def t_constraint(x):
	return 150 - x[2]
rs_const = {'type':'ineq','fun':rs_constraint}
t_const = {'type':'ineq','fun':t_constraint}
par_const = {'type':'ineq','fun':par_constraint}
constraints = [rs_const,t_const]
#
# Objective functions
def uco_obj_fun(x):
	return csa_norm(x) + fs_norm(x) + par_norm(x) + rs_norm(x)
#
# User-constrained overall optimisation
uco_design = minimize(uco_obj_fun,x0,method=opt_method,bounds=opt_bounds,constraints=constraints)
#
# Print results
# print uco_design.x, rsm_models(uco_design.x)
#
# ********************************************************************************
