import parms

from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments

'''
import importlib
importlib.reload(parms)
'''

class dataInputs():

    client = API(access_token=parms.userVals.key) ### Hard coded to location of the key

    #Constructor Method. Inputs to get the data
    def __init__(self, pair, bars, periodocity):
        self.pair = pair
        self.bars = bars
        self.periodocity = periodocity


    # data = dataInputs('EUR_USD', 10, 'D') --> First create variable like this
    #Method for requesting datat with inputs provided
    def periodParms(self):
        parms = {
                "count" : self.bars,
                "granularity" : self.periodocity
        }
        return parms
    # data.periodParms()

    #inputs = dataInputs('EUR_USD', 10, 'D').periodParms()
    def candleInputs(self):
        self.o = instruments.InstrumentsCandles(
                instrument = self.pair,
                params = self.periodParms()
        )
        return self.o

    #data.candleInputs()

    def OHLC(self):

        data = dataInputs(self.pair, self.bars, self.periodocity).client.request(dataInputs(self.pair, self.bars, self.periodocity).candleInputs())

        return data
        #inputs = dataInputs('EUR_USD', 10, 'D')
        #data = inputs.OHLC()

    def Open(self, data):

        open = []
        candle = data['candles']

        for item in candle:
            open.append(item['mid']['o'])
        return open

    def High(self, data):

        high = []
        candle = data['candles']

        for item in candle:
            open.append(item['mid']['h'])
        return high

    def Low(self, data):

        low = []
        candle = data['candles']

        for item in candle:
            low.append(item['mid']['l'])
        return low

    def Close(self, data):
        close = []
        candle = data['candles']

        for item in candle:
            close.append(item['mid']['c'])
        return close

    def getData(self):
        numList = []
        for x in range(0, 10):
            numList.append(self.Close(x))
        return numList
