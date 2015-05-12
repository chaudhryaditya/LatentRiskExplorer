# LatentRiskExplorer

This script pulls data from Quandl to assess Granger causality and correlation between a given response variable (can be a stock, commodity, or other financial instrument), and tens of thousands of other financial instruments so as to discover possible latent risks factors. 

One may find output in the variaous .csv files labelled "gCause_LookAtThisStuffMoreClosely_", followed by the relevant database name

In order to use this script, one need only change the following fields:
  responseVarDataSet (line 45)
  rVName (line 46)

Dependencies:

Quandl (https://www.quandl.com/help/python),
Scipy, 
Numpy,
ystockquote (in folder),
Rpy2,
urllib
