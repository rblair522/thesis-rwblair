## ********************************************************************************
##
##		Design of Experiment (DOE)
##
##		Reads the data from a six factor, half-factorial design of experiment (2^6-1) 
## 		and creates a representative empirical model
##
##		Author: Ross Blair
## 		Date:	30/05/17
##
## ********************************************************************************

## Set working directory
setwd('D:/working_directory')

## ********************************************************************************
##		Read data and define variables
## ********************************************************************************

## Read data, save relevant variables and specify response of interest
m = matrix(scan("doe.dat",skip=1),ncol=11,byrow=TRUE)
response = m[,7]
order = m[,11]

## Save variables as factors
a = as.factor(m[,1])
b = as.factor(m[,2])
c = as.factor(m[,3])
d = as.factor(m[,4])
e = as.factor(m[,5])
f = as.factor(m[,6])

## Save numeric variables and interactions
a = m[,1]
b = m[,2]
c = m[,3]
d = m[,4]
e = m[,5]
f = m[,6]
ef = e*f
de = d*e
df = d*f
cd = c*d
ce = c*e
cf = c*f
bc = b*c
bd = b*d
be = b*e
bf = b*f
ab = a*b
ac = a*c
ad = a*d
ae = a*e
af = a*f

## Create data frame and store table
dafr = data.frame(a,b,c,d,e,f,response,order,
                a,b,c,d,e,f,ef,de,df,cd,ce,cf,bc,bd,be,bf,ab,ac,ad,ae,af)
dafr[,1:8]

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
par(bg=rgb(1,1,0.8),mfrow=c(2,3))
boxplot(response~a, data=dafr, main="Response by a",
        xlab="a",ylab="Response")

boxplot(response~b, data=dafr, main="Response by b",
        xlab="b",ylab="Response")

boxplot(response~c, data=dafr, main="Response by c",
        xlab="c",ylab="Response")

boxplot(response~d, data=dafr, main="Response by d",
        xlab="d",ylab="Response")

boxplot(response~e, data=dafr, main="Response by e",
        xlab="e",ylab="Response")

boxplot(response~f, data=dafr, main="Response by f",
        xlab="f",ylab="Response")
par(mfrow=c(1,1))

## ********************************************************************************
##		ANOVA, Pareto and normal plot of effects (analyse model fit)
## ********************************************************************************

## Fit a model with up to second order interactions
q = aov(response~(a+b+c+d+e+f)^2,data=dafr)
summary(q)

## Save effects in a vector, remove intercept and residuals
qef = q$effects
qef = qef[-1]
qef = qef[(-(length(qef)-9)):(-(length(qef)))]
qefabs = abs(qef)

## Sort effects and save labels
sef = qef[order(qef)]
sefabs = qefabs[order(qefabs)]
qlab = names(sef)

## Generate probability points and theoretical quantiles
pp = ppoints(length(sef))
tq = qnorm(pp)

## Attach quality control charts library
## Generate Pareto chart
library(qcc)
par(bg=rgb(1,1,0.8),mfrow=c(1,1))
qeft = abs(qef)/sqrt(sum(q$residuals^2)*(1/(length(response)/2)))
pareto.chart(qeft, ylab = "Effect", cumperc = seq(0,100, by = 25), 
             main = "Pareto Chart of Effects", col = 1, plot = TRUE)

## t-value selected based on residuals
tval = qt(.95, 9)
abline(h = tval, col=4)
mfrow=c(1,1)

## Generate normal probability plot of effects (excl. residuals and intercept)
par(bg=rgb(1,1,0.8),mfrow=c(1,1))
plot(tq,sef, ylab="Effect", xlab="Theoretical Quantiles",
     main="Normal Plot of Effects")
qqline(sef, col=2)
abline(h=0, col=4)

## Print R squared and adjusted R squared
summary.lm(q)$r.squared
summary.lm(q)$adj.r.squared

## ********************************************************************************
##		Simplify model and fit to the data again (iterative procedure)
## ********************************************************************************

## Remove additional non-significant terms based on p-values
redmod = lm(formula=response~c+d+e+ce, data = dafr)
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
group = rep(1:6,each=length(response))
nstr = rep(response,6)
level = c(m[,1],m[,2],m[,3],m[,4],m[,5],m[,6])
dafrlong = data.frame(group,level,nstr)

## Compute mean, sd, cibar and specify labels
gmn = aggregate(x=dafrlong$nstr,by=list(dafrlong$group,dafrlong$level),FUN="mean")
gsd = aggregate(x=dafrlong$nstr,by=list(dafrlong$group,dafrlong$level),FUN="sd")
cibar = tval*gsd[3]/sqrt(n)
cgroup = rep(c("a","b","c","d","e","f"),2)

## Generate updated data frame
dafrp = data.frame(cgroup,gmn,gsd[3],cibar)
names(dafrp)=c("cgroup","group","level","tmean","std","cibar")

## Attach lattice library and generate main effects plot
library(lattice)
par(bg=rgb(1,1,0.8),mfrow=c(1,1))
xyplot(tmean~level|cgroup,data=dafrp,layout=c(6,1),xlim=c(-2,2),
       ylab="Response",xlab="Coded Factor Levels", type="b",
       panel = function(x, y, ...){
         panel.xyplot(x, y, ...)
         panel.abline(h = mean(response), lty = 2, col = 2)})

## ********************************************************************************