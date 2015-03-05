import urllib
import re
from pprint import *
import Quandl
from  scipy.stats import *
from ystockquote import *
import numpy as np
import time

def main():

        
        dataSetName = 'CURRFX'
                        #OFDP
                        #WSJ
                        #ICE
                        #CURRFX
        
        stockTicker = '^GSPC'   

        #stockFile = open('fordDataOldToNew.txt', 'r')
        stuffToLookAtMoreCloselyFile = open('lookAtThisStuffMoreClosely_' + stockTicker + '_' + dataSetName + '.txt', 'w')
        allCorrelationsFile = open('allCorrelationsFor_' + stockTicker + '_' + dataSetName + '.txt', 'w')

        
        listOfStockData = []

##        for line in stockFile:
##            line = line.strip()
##            listOfStockData.append(float(line))

        dictOfStockPrices = get_historical_prices(stockTicker, '2013-02-28', '2015-02-28')
        listOfDates = list(dictOfStockPrices.keys())
        listOfDates.sort()
        #pprint(listOfDates)
        for date in listOfDates:
                #print(dictOfStockPrices[date]['Close'])
                listOfStockData.append(float(dictOfStockPrices[date]['Close']))

        listOfStockDataChanges = np.diff(listOfStockData) / listOfStockData[:-1]
        

        #pprint(listOfStockData)


        htmltext = 'start'
        pageInt = 1

        startYearRequired = 2012
        updateYearRequired = 2015


        listOfAllDatasetNames = []
        
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
                    print(attributesForThisName)
                   # print(name)
                    
                    startDateString = attributesForThisName[3]
                    print(startDateString)
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
            break

            
            
            
            

        allData = {}
        


        dictOfCorrelationCoefficients = {}

        dictOfStuffToLookAtMoreClosely = {}


        numberOfDataSetsThatWorked = 0
        
        for name in listOfAllDatasetNames:
            attributesForThisName = name.split(',')

            dataForThisDataset = Quandl.get(attributesForThisName[0], trim_start = "2013-02-28", trim_end = "2015-02-28", collapse = 'daily', authtoken="Gps8Po8snGpup7qqsoSm")

            try:
                allData[attributesForThisName[0]] = dataForThisDataset['Settle']

            except:
                    try:
                        allData[attributesForThisName[0]] = dataForThisDataset['Mid']

                    except:
                        try:
                            allData[attributesForThisName[0]] = dataForThisDataset['Level']

                        except:
                                try:
                                        allData[attributesForThisName[0]] = dataForThisDataset['Value']
                                except:
                                        try:
                                                allData[attributesForThisName[0]] = dataForThisDataset['Rate']
                                        except:
                                                continue

            

            #pprint(listOfStockData)
            #pprint( allData[attributesForThisName[0]] )
            #print(len(listOfStockData))
            print(len(allData[attributesForThisName[0]] ))

            dateTimes = list(allData[attributesForThisName[0]].keys())
            listOfDatesForThisDataset = [str(date) for date in dateTimes]
            #print('length should be: ' + str(len(listOfDatesForThisDataset)))

            listOfDatesForThisDataset.sort()
            
            dictOfValuesForThisDataSet = {}

            listOfValuesToUseForThisDataset = []

            listOfStockValuesToUseInConjunctionWithThisDataset = []

            numberOfDatesThatDidntWork = 0

            if abs(len(listOfDatesForThisDataset) - len(listOfDates)) <= 100:

                    #print(attributesForThisName[0])
                    for date in listOfDatesForThisDataset:
                            dateStringForStock = date[: date.rfind('-') + 3]
                            
                            print('For dataset: ' + date)
                            print('For stock: ' + dateStringForStock)
                            #print('Stock price on this date: ' + str(float(dictOfStockPrices[dateStringForStock]['Close'])))

                            #print('Data value on this date: ' + str(float(allData[attributesForThisName[0]][date])))

                            
                            try:                #if the date is in both data sets, add it, otherwise ignore it
                                    dictOfValuesForThisDataSet[date] = [float(dictOfStockPrices[dateStringForStock]['Close']), float(allData[attributesForThisName[0]][date])]

                                    listOfValuesToUseForThisDataset.append(float(allData[attributesForThisName[0]][date]))
                                    
                                    listOfStockValuesToUseInConjunctionWithThisDataset.append(float(dictOfStockPrices[dateStringForStock]['Close']))
                                    

                            except:
                                    numberOfDatesThatDidntWork += 1
                                    #print('Nah')
                                    #print(numberOfDatesThatDidntWork)
                                    continue
                                    
                            

                                    
                                    

                                
                        
                                

                    
            #listOfValuesForThisDataset = allData[attributesForThisName[0]]


            
        
            
            
            print(str(len(listOfValuesToUseForThisDataset)) + ',' + str(len(listOfStockValuesToUseInConjunctionWithThisDataset )))

            #pprint(dictOfValuesForThisDataSet)

            
            #dictOfCorrelationCoefficients[attributesForThisName[0]] = pearsonr(listOfStockData ,  allData[attributesForThisName[0]] )
            
            

            try:
                #listOfDatasetChanges = np.diff(listOfValuesForThisDataset) / listOfValuesForThisDataset[:-1]
                    
                listOfDatasetChanges = np.diff(listOfValuesToUseForThisDataset) / listOfValuesToUseForThisDataset[:-1]
                listOfStockChangesToUseThisTime = np.diff(listOfStockValuesToUseInConjunctionWithThisDataset) / listOfStockValuesToUseInConjunctionWithThisDataset[:-1]

                

                #dictOfCorrelationCoefficients[attributesForThisName[0]] = pearsonr(listOfStockChangesToUseThisTime , listOfDatasetChanges  )

                dictOfCorrelationCoefficients[name] = pearsonr(listOfStockChangesToUseThisTime , listOfDatasetChanges  )
                
                if abs(dictOfCorrelationCoefficients[name][0]) > .6:
                        #dictOfStuffToLookAtMoreClosely[name] = dictOfCorrelationCoefficients[attributesForThisName[0]][0]
                        dictOfStuffToLookAtMoreClosely[name] = dictOfCorrelationCoefficients[name][0]
                #print('Working')

            except:
                #pprint( allData[attributesForThisName[0]] )
                print(name)
                print('Not working')
                continue
            #print(dictOfCorrelationCoefficients[attributesForThisName[0]])
            

            print(len(allData.keys()))

            numberOfDataSetsThatWorked += 1


        pprint(dictOfCorrelationCoefficients)
        pprint(dictOfStuffToLookAtMoreClosely)


        listOfStuffToLookAtMoreCloselyNames = list(dictOfStuffToLookAtMoreClosely.keys())
        
        for dataset in listOfStuffToLookAtMoreCloselyNames:
            stuffToLookAtMoreCloselyFile.write(dataset)
            stuffToLookAtMoreCloselyFile.write('\n')
            stuffToLookAtMoreCloselyFile.write(str(dictOfStuffToLookAtMoreClosely[dataset]))
            stuffToLookAtMoreCloselyFile.write('\n')

        listOfDatasetsThatWorked = list(dictOfCorrelationCoefficients.keys())
        
        for dataset in listOfDatasetsThatWorked:
                allCorrelationsFile.write(dataset)
                allCorrelationsFile.write('\t')
                allCorrelationsFile.write(str(dictOfCorrelationCoefficients[dataset][0]))
                allCorrelationsFile.write('\n')

        
        stuffToLookAtMoreCloselyFile.close()
        stockFile.close()
        allCorrelationsFile.close()

        print(str(numberOfDataSetsThatWorked) + ' out of ' + str(len(allData.keys())) + ' worked')
            
        

if __name__ == "__main__":
        start_time = time.time()
        main()
        print("--- %s seconds ---" % (time.time() - start_time))


