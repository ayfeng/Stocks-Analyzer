import indicator
class SimpleMovingAverageSignal:
    def __init__(self):
        self.signals = []
    def execute(self, prices: [int], stock_indicator: indicator.SimpleMovingAverageIndicator):
        "Determines where the buy and sell signals are for a given list of prices and a type of indicator. Returns a list containing strings equal to BUY, SELL or a blank string and sets the signals attribute of the object to that list."
        result = []
        values = stock_indicator.values
        for i in range(len(values)):
            if values[i] > prices[i] and values[max(0,i-1)] < prices[max(0,i-1)] and i > stock_indicator.days:
                result.append("BUY")
            elif values[i] < prices[i] and values[max(0, i-1)] > prices[max(0,i-1)] and i > stock_indicator.days:
                result.append("SELL")
            else:
                result.append("")
        self.signals = result
        return result

class DirectionalSignal:
    def __init__(self):
        self.signals = []

    def execute(self, prices: [int], stock_indicator: indicator.DirectionalIndicator):
        "Determines where the buy and sell signals are for a given list of prices and a type of indicator. Returns a list containing strings equal to BUY, SELL or a blank string and sets the signals attribute of the object to that list."
        result = []
        buy_threshhold = stock_indicator.buy_threshhold
        sell_threshhold = stock_indicator.sell_threshhold
        for i in range(len(prices)):
            if eval(stock_indicator.values[i]) > buy_threshhold and eval(stock_indicator.values[i-1]) <= buy_threshhold:
                result.append("BUY")
            elif eval(stock_indicator.values[i]) < sell_threshhold and eval(stock_indicator.values[i-1]) >= sell_threshhold:
                result.append("SELL")
            else:
                result.append("")
        self.signals = result
        return result
