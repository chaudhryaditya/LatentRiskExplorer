import urllib
import re
from pprint import *
import Quandl
from  scipy.stats import *
from ystockquote import *
import numpy as np
import time
import Quandl
from rpy2.robjects.packages import importr
import rpy2.robjects as ro

#This script pulls data from Quandl to assess Granger causality and correlation between a given response variable (can be a stock, commodity, or other financial instrument),
#and tens of thousands of other financial instruments so as to discover possible latent risks factors

#One may find output in the variaous .csv files labelled "gCause_LookAtThisStuffMoreClosely_", followed by the relevant database name

#In order to use this script, one need only change the following fields:
#   responseVarDataSet (line 45)
#   rVName (line 46)




def main():
    
    listOfDatabaseNames = ['CBOE', 'OFDP','WSJ','ICE','CURRFX','CRHIS']
    
    for name in listOfDatabaseNames:
        doStuff(name)
    
def doStuff(name):

        #Setup output files, etc
        dataSetName = name #'OFDP'
                        #OFDP
                        #WSJ
                        #ICE
                        #CURRFX
                        #CRHIS
        print('YOOOOOOOOOO STARTING DATABASE: ' + dataSetName)

        
        #stockTicker = '^GSPC'
        responseVarDataSet = '"GOOG/NYSE_FXE"'
        rVName = 'EuroDollarFutures'    #reponse variable name
        
        #stockFile = open('fordDataOldToNew.txt', 'r')
        stuffToLookAtMoreCloselyFile = open('gCause_LookAtThisStuffMoreClosely_' + rVName + 'LONG_' + dataSetName + '.txt', 'w')
        #allCorrelationsFile = open('gCause_AllCorrelationsFor_' + rVName + '_' + dataSetName + '.txt', 'w')

        
        #listOfStockData = []
        
        startDateString = '"2010-02-28"'
        endDateString = '"2015-02-28"'
        
        ro.r('library("Quandl")')
        ro.r('library("tseries")')
        ro.r('library("vars")')


        ro.r('Quandl.auth("Gps8Po8snGpup7qqsoSm")')
        
        
        #Get dataset you want to determine a granger cause for

        print("Quandl(" + responseVarDataSet + ", start_date = " + startDateString +  ", end_date = " + endDateString + ")")
        dataFrameForResponseVar = ro.r("rv = Quandl(" + responseVarDataSet + ",start_date = " + startDateString +  ", end_date = " + endDateString + ")")
        print(dataFrameForResponseVar)
        
        namesForResponseVar  = list(ro.r("names(rv)"))
        
        headerForResponseVar = ''
        
        listOfPossibleHeaders = ['Settle', 'Mid', 'Level', 'Value', 'Rate', 'Adjusted Close', 'Close', rVName]
        
        for possibleHeader in listOfPossibleHeaders:
            if possibleHeader in namesForResponseVar:
                headerForResponseVar = possibleHeader
                break

        print(headerForResponseVar)



        htmltext = 'start'
        pageInt = 1

        startYearRequired = 2012
        updateYearRequired = 2015


        listOfAllDatasetNames = []

        #Get the names of all datasets in this database

        while not htmltext == '':
            print(pageInt)
            url = 'http://www.quandl.com/api/v2/datasets.csv?query=*&source_code=' + dataSetName + '&per_page=300&page=' + str(pageInt) + '&auth_token=Gps8Po8snGpup7qqsoSm'
            htmlfile = urllib.request.urlopen(url)
            #htmltext = htmlfile.read()
            htmltext = htmlfile.read(100000).decode('utf-8')
            listOfDatasetNamesForThisPage = htmltext.split('\n')
           # pprint(listOfDatasetNamesForThisPage)
            for name in listOfDatasetNamesForThisPage:

                try:
                    attributesForThisName = name.split(',')
                    #print(attributesForThisName)
                   # print(name)
                    
                    startDateString = attributesForThisName[3]
                    #print(startDateString)
                    updateDateString = attributesForThisName[len(attributesForThisName) - 1]
                   # print(startDateString)
                    #print(updateDateString)
                    #print(int(updateDateString[:updateDateString.find('-')]))
                        
                    #print('Update year: ' + str(int(updateDateString[:updateDateString.find('-')])))
                    #print('Yo')

                    if int(updateDateString[:updateDateString.find('-')]) >= updateYearRequired and int(startDateString[:startDateString.find('-')]) <= startYearRequired:
                        #print('Yo')                        

                        listOfAllDatasetNames.append(name)

                    else:

                            startDateString = attributesForThisName[2]
                            #print('New start: ' + startDateString)
                            if int(updateDateString[:updateDateString.find('-')]) >= updateYearRequired and int(startDateString[:startDateString.find('-')]) <= startYearRequired:
                                #print('Yo')                        

                                listOfAllDatasetNames.append(name)

                            else:
                                    print('Start year: ' + str(int(startDateString[:startDateString.find('-')]) ))
                                    print('Update year: ' + str(int(updateDateString[:updateDateString.find('-')])))
                            #print('Start year: ' + str(int(startDateString[:startDateString.find('-')]) ))
                            #print('Update year: ' + str(int(updateDateString[:updateDateString.find('-')])))
                            
                
                
                            
                                    
                except:
                    continue

                
            pageInt += 1

            print(len(listOfAllDatasetNames))
        
            

            
            
            
            

        allData = {}
        


        dictOfCorrelationCoefficients = {}

        dictOfStuffToLookAtMoreClosely = {}


        numberOfDataSetsThatWorked = 0
        numberOfDataSetsThatDidntWork = 0
        
        startDateString = '"2013-02-28"'
        endDateString = '"2015-02-28"'

        #For each database, determine if it granger causes the response variable from above

        for name in listOfAllDatasetNames:
            
            attributesForThisName = name.split(',')

            #dataForThisDataset = Quandl.get(attributesForThisName[0], trim_start = "2013-02-28", trim_end = "2015-02-28", collapse = 'daily', authtoken="Gps8Po8snGpup7qqsoSm")
            #print('Quandl("' + attributesForThisName[0] + '" , start_date = ' + startDateString + ' , end_date = ' + endDateString + ' )')
            
            #Get the data for this dataset
            try:
                l = ro.r('possibleCause = Quandl("' + attributesForThisName[0] + '" , start_date = ' + startDateString + ' , end_date = ' + endDateString + ' )')
            except:
                numberOfDataSetsThatDidntWork += 1
                print('NOT WORKING: '+ str(numberOfDataSetsThatDidntWork))
                continue
            #print(l)
            try:
                ro.r('data = merge(rv, possibleCause, by = "Date")')
            except:
                continue
            #print(ro.r('possibleCause'))
            namesForPossibleCause  = list(ro.r("names(possibleCause)"))

            headerForPossibleCause = ''
            
            for possibleHeader in listOfPossibleHeaders:
                if possibleHeader in namesForPossibleCause:
                    headerForPossibleCause = possibleHeader
                    break
            if headerForPossibleCause == '':
                numberOfDataSetsThatDidntWork += 1
                print('NOT WORKING: '+ str(numberOfDataSetsThatDidntWork))
                continue


            #print(headerForPossibleCause)
            #print('Should be about 504: ' + str(len(ro.r('possibleCause$"' + headerForPossibleCause + '"'))))
            #print(ro.r('possibleCause'))
            try:
                if abs( len(ro.r('possibleCause$"' + headerForPossibleCause + '"'))  -  len(ro.r('rv$"' + headerForResponseVar + '"')) > 100):
                    continue
            
            except:
                continue


            #Put all data in 1 matrix
            

            headerForResponseVarNew = headerForResponseVar
            headerForPossibleCauseNew = headerForPossibleCause

            if headerForResponseVar == headerForPossibleCause:
                headerForResponseVarNew += '.x'
                headerForPossibleCauseNew += '.y'



            try:
                #print(ro.r('data'))

                ro.r('possibleCauseValues = as.matrix(data$"' + headerForPossibleCauseNew + '")')
                ro.r('rvValues = as.matrix(data$"' + headerForResponseVarNew + '")')
                l1 = ro.r('data2 = cbind(rvValues, possibleCauseValues)')
                #print(ro.r('data2'))

                #l2 = ro.r('data3 <- apply(data2, 2, rev)')


                ro.r('nr <- nrow(data2)')
                l3 = ro.r('changes = (data2[-1,] - data2[-nr,]) / data2[-nr,]')
                ro.r('colnames(changes) <- c(' + responseVarDataSet + ', "' + attributesForThisName[0] + '")')

                #print(l3)
                #Check for Stationarity in possibleCause dataset
                ro.r('adfTestResForPossibleCause = adf.test(changes[,2])')
                pValueForADF = float(ro.r('adfTestResForPossibleCause$"p.value"')[0])
                if pValueForADF > .05:
                    print('Dataset not stationary, skipping for now')
                    continue

                # print(pValueForADF)

                #Select "optimal" lag using AIC

                lag = int(ro.r('VARselect(changes, type ="none")$"selection"["AIC(n)"]')[0])
                #print(ro.r('VARselect(changes, type ="none")'))

                #print(lag)

                #Fit a VAR to the data
                ro.r('model = VAR(changes, p =' + str(lag) + ' , type = "none")')
                #print(ro.r('model'))


                ro.r('causalityTestResults = causality(model, cause = "' + attributesForThisName[0].replace('/', '.') + '")')
                #print(ro.r('causalityTestResults'))


                pValueForGranger = float(ro.r('causalityTestResults$"Granger"$"p.value"')[0])

                print(pValueForGranger)
                if pValueForGranger < .05:
                    print('Found a granger cause')
                    correl = float(ro.r('correl = cor(changes, use="complete.obs", method="pearson")[2]')[0])
                    print(correl)
                    dictOfStuffToLookAtMoreClosely[name] = [pValueForGranger, correl]
                #stuffToLookAtMoreCloselyFile.write(name  + '\t' + str(pValueForGranger) + '\n')
                numberOfDataSetsThatWorked += 1
                print('WORKING: ' + str(numberOfDataSetsThatWorked))

            except:
                numberOfDataSetsThatDidntWork += 1
                print('NOT WORKING: '+ str(numberOfDataSetsThatDidntWork))
                continue




        listOfStuffToLookAtMoreCloselyNames = list(dictOfStuffToLookAtMoreClosely.keys())
    
        for dataset in listOfStuffToLookAtMoreCloselyNames:
            stuffToLookAtMoreCloselyFile.write(dataset)
            stuffToLookAtMoreCloselyFile.write('\t')
            stuffToLookAtMoreCloselyFile.write(str(dictOfStuffToLookAtMoreClosely[dataset][0]))
            stuffToLookAtMoreCloselyFile.write('\t')
            stuffToLookAtMoreCloselyFile.write(str(dictOfStuffToLookAtMoreClosely[dataset][1]))
            stuffToLookAtMoreCloselyFile.write('\n')
        stuffToLookAtMoreCloselyFile.close()
        
        
#allCorrelationsFile.close()

        print(str(numberOfDataSetsThatWorked) + ' out of ' + str(len(listOfAllDatasetNames)) + ' worked')
            
        

if __name__ == "__main__":
        start_time = time.time()
        main()
        print("--- %s seconds ---" % (time.time() - start_time))


