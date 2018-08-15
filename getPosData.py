##### SCRIPT FOR EXTRATING INFO FROM GET purchase  IN IZETTLE API #####

#online compiler: https://www.onlinegdb.com/online_python_compiler#

import json
from db import connectDatabase
from db import createDatabaseTable
from db import insertPOSDataToDatabase
from db import printDatabaseData
from db import closeDatabase


    
def main():
    apiDataFile = open("apidata.txt").read()
    jsonData = json.loads(apiDataFile)
    
    
    formatAPIDataToTextfile(jsonData)
    
    
    #create database table
    connection = connectDatabase('izettleDatabase.db')
    createDatabaseTable(connection)
    
    
    commonJSONFormat = getCommonJSONFormat(connection, jsonData)
    
    
    filename = "outputFile.txt"                      #name should be a non-exisitng file or empty file
    appendToOutputFile(filename, commonJSONFormat)
    
    printDatabaseData(connection)
    
    
    
    
def getCommonJSONFormat(connection, jsonData):
    dataString = "{\n transactions: \n"
    for purchase in jsonData['purchases']:
        timestamp = purchase['timestamp']
        amount = int(purchase['amount'])/100     #divide by 100 since data is in cents/ører 
        currency = purchase['currency']
        
        #valid payment types are CardPayments, CashPayments, payments (see documentation)
        if ('cashPayments' in purchase):
            paymentType = "cash"
        elif ('cardPayemnts' in purchase):
            paymentType = "card"
        elif ('payment' in purchase):
            paymentType = "other"
            
        
        dictionary = createDictionary(timestamp, amount, currency, paymentType)
        insertPOSDataToDatabase(dictionary, connection)
        
        commonJSONFormat = json.dumps(dictionary, indent=2)         
        dataString += commonJSONFormat
        dataString += "\n"
        
        
        
    dataString += "}"
    return dataString
        
        
        
        
        
        
        
##### UTILITY FUNCTIONS #####        


#strucutre data into a nice format
def formatAPIDataToTextfile(jsonData):
    data = json.dumps(jsonData, indent = 2)
    newFile = open("formattedData.txt", 'w')
    newFile.write(data)
        
        
def appendToOutputFile(filename, data):
    outputFile = open(filename, "a")
    outputFile.write(data)
    outputFile.close()
    
        
def createDictionary(timestamp, amount, currency, paymentType):
    dictionary = {}
    dictionary['timestamp'] = timestamp
    dictionary['amount'] = amount
    dictionary['currency'] = currency
    dictionary['paymentType'] = paymentType
    
    return dictionary
      
      
def testPrinting():
    for purchase in jsonData['purchases']:
        #print(purchase)
        
        #print(purchase['cashPauments'])

        cashPaymentForPurchaseList = purchase['cashPayments']       
        cashPaymentForPurchase = cashPaymentForPurchaseList[0]      #data cashPaymentForPurchase is inside a list with one element
        amount = cashPaymentForPurchase['amount']
        print(amount) #NB, i ører (NOK)
      
        print("\n\n\n")
        
        
        
main()
