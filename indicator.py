class SimpleMovingAverageIndicator:
    def __init__(self, indicator: tuple):
        self.days = indicator[0]
        self.values = []

    def execute(self, prices: [int]):
        "Calculates the indicator values given a list of closing prices. Returns a list of indicator values (floats) and sets the values attribute of the SimpleMovingAverageIndicator equal to that list"
        result = []
        if len(prices):
            for i in range(len(prices)):
                if (i+1) >= self.days:
                    result.append(sum(prices[i-self.days+1:i+1])/self.days)
                else:
                    result.append(0)
        else:
            result.append(0)
        self.values = result

        return result

class DirectionalIndicator:
    def __init__(self, indicator: tuple):
        self.days = indicator[0]
        self.values = []
        self.buy_threshhold, self.sell_threshhold = self._promptForThreshhold()

    def execute(self, prices: [int]):
        "Calculates the indicator values given a list of closing prices. Returns a list of indicator values (floats) and sets the values attribute of the DirectionalIndicator equal to that list"
        result = []
        indicator_values = []
        indicator_values.append("0")
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                indicator_values.append(("+1"))
            elif prices[i] < prices[i-1]:
                indicator_values.append(("-1"))
            else:
                indicator_values.append("0")
        indicator_total = 0
        for i in range(len(prices)):
            indicator_total = sum([eval(value) for value in indicator_values[max(0, i+1-self.days):i+1]])
            result.append(("+" if indicator_total > 0 else "") + str(indicator_total))
        self.values = result
        return result

    def _promptForThreshhold(self) -> (int, int):
        "Prompts the user for a sell and buy threshhold. Returns a tuple of ints containing [0] buy and [1] sell threshhold"
        while True:
            try:
                buy_threshhold = input("What would you like your buy threshhold to be (e.g. +2, -1, -4)?: ")
                int(eval(buy_threshhold))

                sell_threshhold = input("What would you like your sell threshhold to be (e.g. +2, -1, -4)?: ")
                int(eval(sell_threshhold))
                if not(buy_threshhold.startswith("+" or "-") or sell_threshhold.startswith("+" or "-") and (buy_threshhold[1].isdigit() or sell_thresshold[1].isdigit())):
                    raise ValueError
                else:
                    buy_threshhold = int(eval(buy_threshhold))
                    sell_threshhold = int(eval(sell_threshhold))
                    break
            except:
                print("Invalid input. Please enter the threshhold as a number with its corresponding sign (e.g. +4, -1, 0)\n")
        return buy_threshhold, sell_threshhold