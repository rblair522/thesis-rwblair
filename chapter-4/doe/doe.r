## ********************************************************************************
##
##		Design of Experiment
##
##		Reads the data from a three factor, full-factorial design of experiment (2^3) 
## 		and creates a representative empirical model
##
##		Author: Ross Blair
## 		Date:	21/03/18
##
## ********************************************************************************

## Set working directory
setwd('D:/working_directory')

## ********************************************************************************
##		Read data and define variables
## ********************************************************************************

## Read data, save relevant variables and specify response of interest
m = matrix(scan("doe.dat",skip=1),ncol=8,byrow=TRUE)
response = m[,5]
order = m[,8]

## Save variables as factors
a = as.factor(m[,1])
b = as.factor(m[,2])
c = as.factor(m[,3])

## Save numeric variables and interactions
a = m[,1]
b = m[,2]
c = m[,3]

## Create data frame and store table
dafr = data.frame(a,b,c,response)
dafr[,1:4]

## ********************************************************************************
##		Define theoretical model assumptions
## ********************************************************************************

## Assuming n factor and higher order interactions are non-existent

## ********************************************************************************
##		Inspect data
## ********************************************************************************

## Generate four plots
par(bg=rgb(1,1,0.8), mfrow=c(2,2))
qqnorm(response)
qqline(response, col = 2)
boxplot(response, horizontal=TRUE, main="Box Plot", xlab="Response")
hist(response, main="Histogram", xlab="Response")
par(mfrow=c(1,1))

## Assess main effects
par(bg=rgb(1,1,0.8),mfrow=c(1,3))
boxplot(response~a, data=dafr, main="Response by a",
      xlab="a",ylab="Response")

boxplot(response~b, data=dafr, main="Response by b",
      xlab="b",ylab="Response")

boxplot(response~c, data=dafr, main="Response by c",
      xlab="c",ylab="Response")
par(mfrow=c(1,1))

## ********************************************************************************
##		ANOVA
## ********************************************************************************

## Fit a model with up to second order interactions
q = aov(response~(a+b+c)^2,data=dafr)
summary(q)

## Print R squared and adjusted R squared
summary.lm(q)$r.squared
summary.lm(q)$adj.r.squared

## ********************************************************************************
##		Simplify model and fit to the data again (iterative procedure)
## ********************************************************************************

## Remove additional non-significant terms from the stepwise model based on p-values
redmod = lm(response~(a+b),data = dafr)
summary(redmod)

## Print R squared and adjusted R squared
summary.lm(redmod)$r.squared
summary.lm(redmod)$adj.r.squared

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
##		Plots of the main effects
## ********************************************************************************

## Caluclation of t-value
n = length(dafr$response[dafr$a==1])
tval = qt(.95,n-1)

## Rearrange data so that factors and levels are in single columns
group = rep(1:3,each=length(response))
nstr = rep(response,3)
level = c(m[,1],m[,2],m[,3])
dafrlong = data.frame(group,level,nstr)

## Compute mean, sd, cibar and specify labels
gmn = aggregate(x=dafrlong$nstr,by=list(dafrlong$group,dafrlong$level),FUN="mean")
gsd = aggregate(x=dafrlong$nstr,by=list(dafrlong$group,dafrlong$level),FUN="sd")
cibar = tval*gsd[3]/sqrt(n)
cgroup = rep(c("a","b","c"),3)

## Generate updated data frame
dafrp = data.frame(cgroup,gmn,gsd[3],cibar)
names(dafrp)=c("cgroup","group","level","tmean","std","cibar")

## Attach lattice library and generate main effects plot
library(lattice)
par(bg=rgb(1,1,0.8),mfrow=c(1,1))
xyplot(tmean~level|cgroup,data=dafrp,layout=c(3,1),xlim=c(0,4),
       ylab="Response",xlab="Coded Factor Levels", type="b",
       panel = function(x, y, ...){
         panel.xyplot(x, y, ...)
         panel.abline(h = mean(response), lty = 2, col = 2)})

## ********************************************************************************