import sqlite3
#using sqlite - it is possible to export database data from sqlite to a normal sql database


def connectDatabase(databaseFilename):
    #connection = sqlite3.connect(databaseFilename) #izettleData.db
    connection = sqlite3.connect(':memory:')
    return connection

def createDatabaseTable(connection):
    dbCursor = connection.cursor()

    dbCursor.execute("""CREATE TABLE posData (
                amount integer,
                timestamp text,
                paymentType text,
                currency text
                )"""
            )
    
  


 #transaction is in dictionary format 
def insertPOSDataToDatabase(transaction, connection):
    dbCursor = connection.cursor()
    with connection:
        dbCursor.execute("INSERT INTO posData VALUES (:amount, :timestamp, :paymentType, :currency)",
                        {'amount': transaction.get('amount'), 'timestamp': transaction.get('timestamp'), 'paymentType': transaction.get('paymentType'), 'currency': transaction.get('currency')}
                        )
    
    
    
def printDatabaseData(connection):
    dbCursor = connection.cursor()
    dbCursor.execute("SELECT * FROM posData")
    print(dbCursor.fetchall())
    
    
#def returnDatabaseDataBetweenTimePoints(stard, end, ..)

#def returnDataBaseWith
  
  
def closeDatabase(connection):
    connection.commit()
    connection.close()


#############################

def test():
    conn = connectDatabase('izettleData.db')
    createDatabaseTable(conn)

    amount1 = 500
    payType1 = "card"
    currency1 = "SEK"
    timestamp1 = "09.12.2018"
    transactionDict1 = {'amount':amount1, 'paymentType': payType1, 'currency': currency1, 'timestamp':timestamp1}

    amount2 = 273
    payType2 = "cash"
    currency2 = "NOK"
    timestamp2 = "02.11.2018"
    transactionDict2 = {'amount':amount2, 'paymentType': payType2, 'currency': currency2, 'timestamp':timestamp2}

    insertPOSDataToDatabase(transactionDict1, conn)
    insertPOSDataToDatabase(transactionDict2, conn)
    returnDatabaseData(conn)
    closeDatabase(conn)




#test()


