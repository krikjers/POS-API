#SQLite is good for Small to medium apps, testing and prototyping. Simple to port over to larger database.
#Database can be in memory, a file etc

#https://www.youtube.com/watch?v=pd-0G0MigUA



#
import sqlite3

#can store data in 'memory' or in a file name. file name used here.
#connect creates the file if it does not exist, and just connect if it does exist.
#conn = sqlite3.connect('izettleData.db') 

#make database that runs in RAM, useful since don't need to delete database file between every compilation
conn = sqlite3.connect(':memory:')



#make a cursor, allows us to execute sql comamnds
#cursor is a control stucture that enables traversal over records in a database
c = conn.cursor()

# three " lets us make multiline strings"
#amount is name of first column, timestamp is 2. column etc. must make it a data type. example: NULL; INTEGER; REAL; TEXT; BLOB
#note: gives error if the table already exist (can run this code only once)
#CREATE TABLE is an SQL command
c.execute("""CREATE TABLE posData (
            amount integer,
            timestamp text,
            paymentType text,
            currency text
            )""")
    
 ######## insert data 
#insert data into posData table as a row . INSERT INTO is an SQL command 
c.execute("INSERT INTO posData VALUES (500, '07.09.2018', 'cash', 'NOK')")
conn.commit()

amount1 = 200
timestamp1 = "13.10.2018"
paymentType1 = "creditCard"
currency1 = "NOK"

#bad way: vulnerable to sql injection
#c.execute("INSERT INTO posData VALUES ({}, '{}', '{}', '{}')".format(amount1, timestamp1, paymentType1, currency1))

#good way:  ? are place holders for values in the tuple argument
#c.execute("INSERT INTO posData VALUES (?, ?, ?, ?)", (amount1, timestamp1, paymentType1, currency1))

#good way number 2. use a dictionary instead of tuple as argument. dictionary keys are the names of the place holdesr
#c.execute("INSERT INTO posData VALUES (:amount, :timestamp, :paymentType, :currency)", 
#                                        {'amount': amount1, 'timestamp': timestamp1, 'paymentType': paymentType1, 'currency': currency1} )


conn.commit()







    
########### functions

amount1 = 200
timestamp1 = "13.10.2018"
paymentType1 = "creditCard"
currency1 = "NOK"
transaction1 = {'amount':amount1, 'timestamp':timestamp1, 'paymentType':paymentType1, 'currency': currency1}

amount2 = 350
timestamp2 = "03.02.2018"
paymentType2 = "creditCard"
currency2 = "SEK"
transaction2 = {'amount':amount2, 'timestamp':timestamp2, 'paymentType':paymentType2, 'currency': currency2}

#print(transaction.get('amount'))

def insert_transaction(transaction):
    with conn:
        c.execute("INSERT INTO posData VALUES (:amount, :timestamp, :paymentType, :currency)", 
                                        {'amount': transaction.get('amount'), 'timestamp': transaction.get('timestamp'), 'paymentType': transaction.get('paymentType'), 'currency': transaction.get('currency')} )
    #with conn: code: connection object can be used as a context maanger to automatically commit or roll back transaction. transaction will be commited unless there is a tranasction. we dont need to write conn.commit()
    
def get_transaction_by_amount(amountArg):
    c.execute("SELECT * FROM posData WHERE amount=:amount", {'amount': amountArg}  )
    #select does not need to be commited
    return c.fetchall()
    
    
def update_transaction_currency(transaction, newCurrency):
    with conn:
        c.execute(""" UPDATE posData SET currency = :currency
                        WHERE  amount = :amount AND paymentType = :paymentType """,
                        {'amount': transaction.get('amount'), 'currency': transaction.get('currency'), 'paymentType': transaction.get('paymentType')} 
                )

def remove_tranasction(transaction):
    with conn:
        c.execute("DELETE from posData WHERE amount = :amount",
                 {'amount':transaction.get('amount')}
                 )
    
    
insert_transaction(transaction1)
insert_transaction(transaction2)




########### fetch data

#by having a WHERE keyword, we can select what kind of rows we want. there are many ways to do the same thing:
#c.execute("SELECT * FROM posData WHERE amount = 200")  
#c.execute("SELECT * FROM posData WHERE amount=?", (500,))
#c.execute("SELECT * FROM posData WHERE amount=:amount", {'amount': 500}  )

c.execute("SELECT * FROM posData")



#return next row (gives none if no rows to fetch)
#print(c.fetchone())
print(c.fetchall()) #gives all rows placed inside a list
#print(c.fetchmany(5)) #fetch 5 rows
    
    
    
    

    

#commit changes to database
conn.commit()

#close connection
conn.close()
