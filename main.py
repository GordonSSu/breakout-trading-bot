import numpy as np

class CrawlingRedOrangePenguin(QCAlgorithm):

    def Initialize(self):
        # Set starting cash balance to 1m for backtesting purposes
        self.SetCash(1000000)
        
        # Set start and end dates for backtesting purposes
        self.SetStartDate(2015, 11, 11)
        self.SetEndDate(2018, 11, 11)
        
        # Add asset to algorithm; track the S&P 500 Index
        self.symbol = self.AddEquity("SPY", Resolution.Minute).Symbol
        
        # Set lookback length (and upper/lower bounds) for determining breakout level
        self.lookback = 20
        self.lookbackLowerLimit = 10
        self.lookbackUpperLimit = 30
        
        self.initialStopRisk = 0.98
        self.trailingStopRisk = 0.9
        
        self.Schedule.On(self.DateRules.EveryDay(self.symbol), \
                self.TimeRules.AfterMarketOpen(self.symbol, 20), \
                Action(self.EveryMarketOpen))


    def EveryMarketOpen(self):
        close = self.History(self.symbol, 31, Resolution.Daily)["close"]
        todaysVolatility = np.std(close[1:31])
        yesterdaysVolatility = np.std(close[0:30])
        volatilityDelta = (todaysVolatility - yesterdaysVolatility) / todaysVolatility
        self.lookback = round(self.lookback * (1 + volatilityDelta))
        
        # Ensure that lookback length falls between upper and lower limits
        if number not in range(self.lookbackLowerLimit, self.lookbackUpperLimit + 1):
            self.lookback = self.lookbackLowerLimit if self.lookBack < self.lookbackLowerLimit else self.lookbackUpperLimit
        
        self.high = self.History(self.symbol, self.lookback, Resolution.Daily)["high"]
        
        if not self.Securities[self.symbol].Invested and \
                self.Securities[self.symbol].Close >= max(self.high[:-1]):
            self.SetHoldings(self.symbol, 1)
            self.breakoutLevel = max(self.high[:-1])
            self.highestPrice = self.breakoutLevel
            
        if self.Securities[self.symbol].Invested:
            if not self.Transactions.GetOpenOrders(self.symbol):
                self.stopMarketTicket = self.StopMarketOrder(self.symbol, \
                        -self.Portfolio[self.symbol].Quantity, \
                        self.initialStopRisk * self.breakoutLevel)
                
            if self.Securities[self.symbol].Close > self.highestPrice and \
                    self.initialStopRisk * self.breakoutLevel < \
                    self.Securities[self.symbol].Close * self.trailingStopRisk:
                self.highestPrice = self.Securities[self.symbol].Close
                updateFields - UpdateOrderFields()
                updatefields.StopPrice = self.Securities[self.symbol].Close * self.trailingStopRisk
                self.stopMarketTicket.Update(udpateFields)
                
                # Print new stop price to console so we can track the new order price every time it updates
                self.Debug(updateFields.StopPrice)
                
            # Plot the stop price of our position onto the data chart
            self.Plot("Data Chart", "Stop Price", self.stopMarketTicket.Get(OrderField.StopPrice))


    def OnData(self, data):
        self.Plot("Data Chart", self.symbol, self.Securities[self.symbol].Close)
