class Signal:
    def __init__(self):
        import indicator
        self.signals = []
    def execute(self, prices: [int], stock_indicator: indicator.Indicator):
        result = []
        if stock_indicator.type = "s":
            values = stock_indicator.values[stock_indicator.days+1:-1]
            for i in range(len(values)):
                if values[i] > prices[i] and values[i-1] < prices[i-1]:
                    result.append("BUY")
                elif values[i] < prices[i] and values[i-1] > prices[i-1]:
                    result.append("SELL")
                else:
                    result.append("")
        elif stock_indicator.type = "d":
            pass
        self.signals = result
        return result

    def getValues():
        return self.signals

