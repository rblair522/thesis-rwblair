## ********************************************************************************
##
##		Response Surface Methodology (RSM)
##
##		Reads the data from a response surface matrix and creates a representative
## 		empirical model
##
##		Author: Ross Blair
## 		Date:	22/06/17
##
## ********************************************************************************

## Set working directory
setwd('D:/working_directory')

## ********************************************************************************
##		Read data and define variables
## ********************************************************************************

## Read data, save relevant variables and specify response of interest
m = matrix(scan("lhc.dat",skip=1),ncol=9,byrow=TRUE)
response = m[,6]
order = m[,9]

## Save variables as factors
a = as.factor(m[,1])
b = as.factor(m[,2])
c = as.factor(m[,3])
d = as.factor(m[,4])

## Save numeric variables and interactions
a = m[,1]
b = m[,2]
c = m[,3]
d = m[,4]
cd = c*d
bc = b*c
bd = b*d
ab = a*b
ac = a*c
ad = a*d
aa = a*a
bb = b*b
cc = c*c
dd = d*d

## Create data frame and store table
dafr = data.frame(a,b,c,d,response,order)
dafr[,1:6]

## ********************************************************************************
##		Inspect data
## ********************************************************************************

## Generate four plots
par(bg=rgb(1,1,0.8), mfrow=c(2,2))
qqnorm(response)
qqline(response, col = 2)
boxplot(response, horizontal=TRUE, main="Box Plot", xlab="Response")
hist(response, main="Histogram", xlab="Response")
plot(order, response, xlab="Actual Run Order", ylab="Response",
     main="Run Order Plot")
par(mfrow=c(1,1))

## Assess main effects
par(bg=rgb(1,1,0.8),mfrow=c(1,4))
boxplot(response~a, data=dafr, main="Response by a",
        xlab="a",ylab="Response")

boxplot(response~b, data=dafr, main="Response by b",
        xlab="b",ylab="Response")

boxplot(response~c, data=dafr, main="Response by c",
        xlab="c",ylab="Response")

boxplot(response~d, data=dafr, main="Response by d",
        xlab="d",ylab="Response")
par(mfrow=c(1,1))

## ********************************************************************************
##		ANOVA, Pareto and normal plot of effects (analyse model fit)
## ********************************************************************************

## Fit a model with up to second order interactions
q = lm(response~(a+b+c+d)^2,data = dafr)
summary(q)

## ********************************************************************************
##		Simplify model and fit to the data again (iterative procedure)
## ********************************************************************************

## Remove additional non-significant terms from the stepwise model based on p-values
redmod = lm(response~a+b+c+d+ab+ac+ad+bc+bd+cd+aa+bb+cc+dd,data = dafr)
# redmod = lm(response~c+ad+bd+cd,data = dafr)
summary(redmod)

## ********************************************************************************
##		Analyse model fit
## ********************************************************************************

## Plot standardised residuals versus predicted response
pred_resp = predict(redmod)
pred_resp_df = as.data.frame(pred_resp)
r_std = rstandard(redmod)
r_std_df = as.data.frame(r_std)
pred_resp_r_std_df = rbind(pred_resp, r_std)
pred_resp_r_std_df = t(pred_resp_r_std_df)
par(bg=rgb(1,1,0.8))
plot(pred_resp,r_std,ylab="Residual",
     xlab="Predicted Response")
abline(h=0)
par(mfrow=c(1,1))

## Generate probability points and theoretical quantiles
pp = ppoints(length(redmod$residuals))
tq = qnorm(pp)

## Generate four plots
par(bg=rgb(1,1,0.8), mfrow=c(2,2))
qqnorm(redmod$residuals)
qqline(redmod$residuals, col=2)
abline(h=0)
boxplot(redmod$residuals, horizontal=TRUE, main="Box Plot", xlab="Residual")
hist(redmod$residuals, main="Histogram", xlab="Residual")
plot(order, redmod$residuals, xlab="Actual Run Order", ylab="Residual",
     main="Run Order Plot")
par(mfrow=c(1,1))

## ********************************************************************************