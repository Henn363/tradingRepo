from parms import userVals
from candles import dataInputs
import database as db

from datetime import datetime

'''
import importlib
importlib.reload(db)

'''

db_file = '/Users/mhenning/grids.db'

class query():

    def get_pairs():
        #Get all the table names
        q = ''' SELECT *
        FROM sqlite_master
        WHERE type = 'table'
        AND name != 'sqlite_sequence'
        '''

        pairs = db.DB(db_file).query(q)['tbl_name'].values.tolist()
        return pairs

    def currentgridPx(pair): #pair = 'EUR_USD'

        q = ''' SELECT *
        FROM {}
        ORDER BY `id` DESC
        LIMIT 1
        '''.format(pair)

        resPx = db.DB(db_file).query(q)

        return resPx
    def checkgrid(pair):

        #Save the current Date
        t = datetime.now().date()

        #Get last grid entry for this product
        last = db.DB(db_file).currentgridPx(pair)

    def insertNewGridLevel(pair, id, time, lastClose, direction):

        #Shift Grid Up
        q = ''' INSERT INTO {}
        VALUES({}, '{}', {}, '{}')
        '''.format(pair, id, time, float(lastClose), direction)

        db.DB(db_file).updateTable(q)
