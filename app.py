#Import modules
from parms import userVals
from candles import dataInputs
from Trade import Trade


import database as db
import queries
import pandas as pd


from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.contrib.requests import MarketOrderRequest
from oandapyV20.contrib.requests import LimitOrderRequest
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.trades as trades

from datetime import datetime
import time
from decimal import Decimal
import numpy

'''
import importlib
importlib.reload(Trade)


Functions.getLevels('EUR_USD', 'Long')
'''

db_file = '/Users/mhenning/grids.db'
spacing = 1 / 1000

#Create a class to define everything that happens to update grid levels
count = 0

while True:

    try:

        time.sleep(60)

        #Get all the table names
        q = ''' SELECT *
        FROM sqlite_master
        WHERE type = 'table'
        AND name != 'sqlite_sequence'
        '''

        pairs = db.DB(db_file).query(q)['tbl_name'].values.tolist()
        count += 1

            #Create a dataframe with this info
        cols = ['Pair', 'Price', 'Initial Position', 'Current Position']
        df = pd.DataFrame(columns = cols)


        #pair = 'EUR_USD'
        for pair in pairs:
            print(pair)

            #Iterate over each pair and see if the grid needs to be upda        for pair in pairs:
            print('Checking Pair: {} {}'.format(pair,count))

            #Get previous grid px
            GridPx = queries.query.currentgridPx(pair)
            lastGridPx = queries.query.currentgridPx(pair)['gridPx'][0]

            #Check if the grid needs to be update. Get latest price
            lastBar = dataInputs(pair, 1, 'M1').OHLC()['candles'][0]['mid']
            lastBarRange = numpy.arange(float(lastBar['l']), float(lastBar['h']), 0.00001)
            print('High : {} - Low : {}'.format(lastBar['h'],lastBar['l']))

            #Get the ticks in 10 ticks intervals.
            #tickIntervals = tickIntervals.append(0.639) #lastBarRange
            tickIntervals = []

            #tickIntervals.append(1.085)
            for bar in lastBarRange:
                bar = round(bar,5)
                if len(str(bar)) == 5:
                    tickIntervals.append((bar))

            #Get Open Positions for this Pair
            trades = Trade().getOpenTrades()

            for trade in trades['trades']:
                #print(trade)
                p = trade['instrument']
                px = trade['price']
                pos = trade['initialUnits']
                curPos = trade['currentUnits']

                temp = pd.DataFrame(columns = cols)
                temp = temp.append({
                        'Pair' : p,
                        'Price' : px,
                        'Initial Position' : pos,
                        'Current Position' : curPos
                        }, ignore_index = True)

                df = df.append(temp)

            #Filter only positions for this pair
            df = df[df.Pair == pair]

            if len(tickIntervals) > 0:
                px = round(tickIntervals[0], 4)

                if float(px) != float(lastGridPx):
                    #Check Open Orders for anyopen orders at this price

                    if px not in df.Price.values.tolist():

                        client = API(access_token = userVals.key)

                        #enter trade
                        if float(px) > float(lastGridPx):

                            #Uptick. Calculate total buy positions
                            Units =  Trade().UnitsAvailable(pair, 'Long')
                            Trade().openLong(pair, px)


                            print('Bought {} units at {}'.format(Units, px))

                        else:
                                                        #Define STop/Profit prices
                            Units = Trade().UnitsAvailable(pair, 'Short')

                            Trade().openShort(pair, px)
                            print('Sold {} units at {}'.format(Units, px))



                                                    #Define some variables
                        t = str(datetime.now())
                        id = GridPx.id[0] + 1

                        direction = ''

                        #If its an uptick
                        if float(px) > float(lastGridPx):
                            direction = 'Up'
                        else:
                            direction = 'Down'

                        #Update the Table
                        queries.query.insertNewGridLevel(pair, id, t , float(px), direction)

                    else:
                        print('Position exists at {}'.format(px))



                    print('Pair : {}'.format(pair))
                    print('New Grid Level: {}, Direction : {}'.format(px, direction))

                else:
                    print("Grid Px {} is same as last Px {}".format(px, lastGridPx))



    except Exception as e:
        print(e)
