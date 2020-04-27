from oandapyV20 import API
import oandapyV20
from oandapyV20.contrib.requests import LimitOrderRequest
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.trades as trades


from parms import userVals
import random


import pandas as pd

'''
import importlib
importlib.reload(functions)


'''

class Trade():

    #Class Variables Client.
    client = API(access_token = userVals.key)
    spacing =  1 / 1000


    def getTrades(self):
      r = accounts.AccountDetails(userVals.accountID)
      client = API(access_token=userVals.key)
      rv = client.request(r)
      self.details = rv.get('account')
      return self.details.get('openTradeCount')

      #Trade().getTrades()


    def getOpenTrades(self):
        r = trades.OpenTrades(accountID = userVals.accountID)
        client = API(access_token = userVals.key)
        rv = client.request(r)

        return rv

        #Trade().getOpenTrades()
    #pair = 'AUD_USD'
    #Side = 'Long'
    def UnitsAvailable(self, pair, Side):
        Side = Side
        pair = pair


        trades = Trade().getOpenTrades()

        if len(trades['trades']) > 0:

            cols = ['Pair', 'Price', 'Initial Position', 'Current Position']
            df = pd.DataFrame(columns = cols)

            temp = pd.DataFrame(columns = cols)


            for trade in trades['trades']:
                print(trade)
                if trade['state'] == 'OPEN':
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

            df = df[df.Pair == pair]

            if Side == 'Long':
                df = df[df['Current Position'].astype(int)  > 0]
                return 100000 - df['Current Position'].astype(int).sum()
            else:
                df = df[df['Current Position'].astype(int) < 0]
                return 100000 + df['Current Position'].astype(int).sum()

        else:
            return 100000

    #price = Trade().UnitsAvailable('EUR_USD', 'Short')
    #pair = 'EUR_USD'
    #price = 1.2324
    def openLong(self, pair, price) :

        #Calc Profit and Stop Order
        client = API(access_token = userVals.key)
        spacing =  1 / 1000
        takeProfitPx = price + spacing
        takeStopPx = price - spacing

        random.seed(3)

        # print a random number between 1 and 1000.
        randint = random.uniform(.95, 1)

        units = int(Trade().UnitsAvailable(pair, 'Long') * randint)

        if units > 0:

            lmtOrderLong1 = LimitOrderRequest(
                            instrument = pair,
                            price = price,
                            units = int(units / 2),
                            takeProfitOnFill = TakeProfitDetails(price = takeProfitPx ).data,
                            stopLossOnFill = StopLossDetails(price = takeStopPx).data)

            r = orders.OrderCreate(userVals.accountID , data = lmtOrderLong1.data)
            client.request(r)

            #print('Bought {} units of {} at {} '.format(units, pair, price))


            lmtOrderLong2 = LimitOrderRequest(
                            instrument = pair,
                            price = price,
                            units = int(units / 4),
                            takeProfitOnFill = TakeProfitDetails(price = takeProfitPx + spacing ).data,
                            stopLossOnFill = StopLossDetails(price = takeStopPx).data)

            r = orders.OrderCreate(userVals.accountID , data = lmtOrderLong2.data)
            client.request(r)


            lmtOrderLong3 = LimitOrderRequest(
                            instrument = pair,
                            price = price,
                            units = int(units / 8),
                            takeProfitOnFill = TakeProfitDetails(price = takeProfitPx  + (spacing * 2)).data,
                            stopLossOnFill = StopLossDetails(price = takeStopPx).data)

            r = orders.OrderCreate(userVals.accountID , data = lmtOrderLong3.data)
            client.request(r)


            lmtOrderLong4 = LimitOrderRequest(
                            instrument = pair,
                            price = price,
                            units = int(units / 8.01),
                            takeProfitOnFill = TakeProfitDetails(price = takeProfitPx  + (spacing * 3)).data,
                            stopLossOnFill = StopLossDetails(price = takeStopPx).data)

            r = orders.OrderCreate(userVals.accountID , data = lmtOrderLong4.data)
            client.request(r)

            #print('Bought {} units '.format(units))

            #Trade().openLong('EUR_USD', 1.086)
            # price = 1.081
            # pair = 'EUR_USD'
    def openShort(self, pair, price) :

        #Calc Profit and Stop Order
        client = API(access_token = userVals.key)
        spacing =  1 / 1000
        takeProfitPx = round(price - spacing, 4)
        takeStopPx = round(price + spacing , 4)


        # print a random number between 1 and 1000.
        randint = random.uniform(.9, 1)

        units = int(Trade().UnitsAvailable(pair, 'Short') * randint)


        if units > 0:


            lmtOrderShort1 = LimitOrderRequest(
                            instrument = pair,
                            price = price,
                            units = int(units / 2) * -1 ,
                            takeProfitOnFill = TakeProfitDetails(price = takeProfitPx ).data,
                            stopLossOnFill = StopLossDetails(price = takeStopPx).data)

            r = orders.OrderCreate(userVals.accountID , data = lmtOrderShort1.data)
            client.request(r)


            lmtOrderShort2 = LimitOrderRequest(
                            instrument = pair,
                            price = price,
                            units = int(units / 4) * -1,
                            takeProfitOnFill = TakeProfitDetails(price = takeProfitPx - spacing ).data,
                            stopLossOnFill = StopLossDetails(price = takeStopPx).data)

            r = orders.OrderCreate(userVals.accountID , data = lmtOrderShort2.data)
            client.request(r)


            lmtOrderShort3 = LimitOrderRequest(
                            instrument = pair,
                            price = price,
                            units = int(units / 8) * -1,
                            takeProfitOnFill = TakeProfitDetails(price = takeProfitPx  - (spacing * 2)).data,
                            stopLossOnFill = StopLossDetails(price = takeStopPx).data)

            r = orders.OrderCreate(userVals.accountID , data = lmtOrderShort3.data)
            client.request(r)


            lmtOrderShort4 = LimitOrderRequest(
                            instrument = pair,
                            price = price,
                            units = int(units / 8.01) * -1,
                            takeProfitOnFill = TakeProfitDetails(price = takeProfitPx  - (spacing * 3)).data,
                            stopLossOnFill = StopLossDetails(price = takeStopPx).data)

            r = orders.OrderCreate(userVals.accountID , data = lmtOrderShort4.data)
            client.request(r)
