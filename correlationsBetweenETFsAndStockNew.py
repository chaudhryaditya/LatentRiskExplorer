import urllib
import re
from pprint import *
import Quandl
from  scipy.stats import *
from ystockquote import *
import numpy as np
import time

def main():


        dataSetName = 'ETFs'
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
                listOfStockData.append(float(dictOfStockPrices[date]['Adj Close']))

        listOfStockDataChanges = np.diff(listOfStockData) / listOfStockData[:-1]



        
        etfSymbolsFile = open('listOfETFSymbols.txt', 'r')

        dictOfETFs = {}

        for line in etfSymbolsFile:
            line = line.strip()
            dictOfETFs[line] = []

        listOfETFNames = list(dictOfETFs.keys())
        listOfETFNames.sort()

        #pprint(listOfETFNames)

        weAreOnTheIthETFNow = 0

        for etf in listOfETFNames:
                
                weAreOnTheIthETFNow += 1
                print(weAreOnTheIthETFNow)
                try:
                        historicalDict = get_historical_prices(etf, '2013-02-28', '2015-02-28')

                except:
                        continue

                listOfHistoricalPrices = []

                dates = list(historicalDict.keys())
                dates.sort()
            
                for date in dates:
                        dictOfETFs[etf].append(float(historicalDict[date]['Adj Close']))
                

        dictOfCorrelationCoefficients = {}
        dictOfStuffToLookAtMoreClosely = {}

        
        #pprint(dictOfETFs)
        #return

        numberThatDidntWork = 0
        
        for etf in listOfETFNames:
                listOfDailyClosesForThisETF = dictOfETFs[etf]

                

                try:
                        listOfDailyClosesForThisETF = dictOfETFs[etf]

                        
                        #listOfDatasetChanges = np.diff(listOfValuesForThisDataset) / listOfValuesForThisDataset[:-1]
                            
                        listOfETFChanges = np.diff(listOfDailyClosesForThisETF) / listOfDailyClosesForThisETF[:-1]
                        listOfStockChangesToUseThisTime = np.diff(listOfStockData) / listOfStockData[:-1]

                        

                        dictOfCorrelationCoefficients[etf] = pearsonr(listOfStockChangesToUseThisTime , listOfETFChanges  )
                        
                        if abs(dictOfCorrelationCoefficients[etf][0]) > .6:
                            dictOfStuffToLookAtMoreClosely[etf] = dictOfCorrelationCoefficients[etf][0]
                        print('Working')

                except:
                        #pprint( allData[attributesForThisName[0]] )
                        print(etf)
                        print('Not working')
                        numberThatDidntWork += 1
                        continue
                
            #print(dictOfCorrelationCoefficients[attributesForThisName[0]])
            
        pprint(dictOfCorrelationCoefficients)
        pprint(dictOfStuffToLookAtMoreClosely)


        listOfStuffToLookAtMoreCloselyNames = list(dictOfStuffToLookAtMoreClosely.keys())
        
        for etf in listOfStuffToLookAtMoreCloselyNames:
                stuffToLookAtMoreCloselyFile.write(etf)
                stuffToLookAtMoreCloselyFile.write('\n')
                stuffToLookAtMoreCloselyFile.write(str(dictOfStuffToLookAtMoreClosely[etf]))
                stuffToLookAtMoreCloselyFile.write('\n')


        listOfETFNamesThatWorked = list(dictOfCorrelationCoefficients.keys())
        
        for etf in listOfETFNamesThatWorked:
                allCorrelationsFile.write(etf)
                allCorrelationsFile.write('\t')
                allCorrelationsFile.write(str(dictOfCorrelationCoefficients[etf][0]))
                allCorrelationsFile.write('\n')

        
        stuffToLookAtMoreCloselyFile.close()
        stockFile.close()
        allCorrelationsFile.close()

        print(str(numberThatDidntWork) + ' out of ' + str(len(dictOfETFs.keys())) + " didn't work")

            
        

if __name__ == "__main__":
        start_time = time.time()
        main()
        print("--- %s seconds ---" % (time.time() - start_time))


