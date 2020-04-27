import sqlite3
from sqlite3 import Error
import pandas as pd

''' Hard code the local sql lite db '''

db_file = '/Users/mhenning/grids.db'


class DB():

    #Hard code the path to the database
    db_file = '/Users/mhenning/grids.db'

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        #print('Connection Succesful')

    def query(self, query):

        try:

            # Instantitate the cursor
            mycursor = self.conn.cursor()

            # Fetch the results
            mycursor.execute(query)
            res = mycursor.fetchall()

            # Return results as a dataframe
            DF = pd.DataFrame(res, columns= [description[0] for description in mycursor.description])
            return(DF)

            # Close the Connection
            mycursor.close()
            self.conn.close()
        except Exception as e:
            print(e)


    def create_table(self, tableName): #tableName = 'EUR_USD'

        try:

            #instantiate a cursor
            mycursor = self.conn.cursor()

            #Define the query
            q = ''' CREATE TABLE IF NOT EXISTS {}
            (`id`, `dateTime` TEXT, `tradePx` REAL, `gridLevel` REAL, `bidgridLevel` REAL, `askgridLevel` REAL)
            '''.format(tableName)

            #Execute the query
            mycursor.execute(q)

            #Commit Statement to the database
            self.conn.commit()

            #Now close the connection
            mycursor.close()
            self.conn.close()

        except Exception as e:
            print(e)


    def updateTable(self, q): # q = "INSERT INTO EUR_USD VALUES(1, '2020-01-01 00:00:00', 1.23456, 1.23460, 1.23455, 1.23465)"

        try:

            #instantiate a cursor
            mycursor = self.conn.cursor()

            #Execute the query
            mycursor.execute(q)

            #Commit Statement to the database
            self.conn.commit()

            #Now close the connection
            mycursor.close()
            self.conn.close()

        except Exception as e:
            print(e)
