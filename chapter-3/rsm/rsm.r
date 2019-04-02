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
m = matrix(scan("rsm.dat",skip=1),ncol=7,byrow=TRUE)
response = m[,6]
order = m[,7]

## Save variables as factors
a = as.factor(m[,1])
b = as.factor(m[,2])

## Save numeric variables and interactions
a = m[,1]
b = m[,2]
ab = a*b
aa = a*a
bb = b*b

## Create data frame and store table
dafr = data.frame(a,b,ab,aa,bb,response,order)
dafr[,1:7]

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
par(bg=rgb(1,1,0.8),mfrow=c(1,2))
boxplot(response~a, data=dafr, main="Response by a",
        xlab="a",ylab="Response")

boxplot(response~b, data=dafr, main="Response by b",
        xlab="b",ylab="Response")
par(mfrow=c(1,1))

## ********************************************************************************
##		ANOVA, Pareto and normal plot of effects (analyse model fit)
## ********************************************************************************

## Fit a model with up to second order interactions
library(rsm)
q = rsm(response~SO(a,b),data=dafr)
summary(q)

## ********************************************************************************
##		Simplify model and fit to the data again (iterative procedure)
## ********************************************************************************

## Remove additional non-significant terms based on p-values
redmod = lm(response~a+b,data = dafr)
summary(redmod)

## ********************************************************************************
##		Analyse residual graphs
## ********************************************************************************

## Plot residuals versus predicted response
par(bg=rgb(1,1,0.8))
plot(predict(redmod),redmod$residuals,ylab="Residual",
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
##		Contour plots of the response variable
## ********************************************************************************

## 2D plot
par(bg=rgb(1,1,0.8), mfrow=c(1,1))
contour(redmod, b ~ a, col="blue")
mfrow=c(1,1)

## ********************************************************************************