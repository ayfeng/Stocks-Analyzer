import connectToURL, stock_signal, indicator, datetime, time, collections, urllib.request, re
from time import strftime
from urllib.error import HTTPError
from collections import namedtuple

#TODO: Make chart go in ascending order

QueryData = namedtuple("QueryData", ["symbol", "start", "end", "indicator"])
Stock = namedtuple("Stock", ["date", "close", "indicator", "signal"])

class InvalidDateFormatError(Exception):
    def __init__(self, date_string: str):
        self.msg = "The format in which the date was entered is incorrect (" + date_string +"). Dates should be entered in a YYYY-MM-DD format."


def _printChart(query: QueryData, stockList: [Stock], indicator_and_signal: tuple) -> str:
    "Print a chart of the stock data"

    # stock_indicator, signal = indicator_and_signal
    # indicator_values = stock_indicator.execute(stock_prices)
    # signal_values = signal.execute(stock_prices, stock_indicator)
    the_indicator = indicator_and_signal[0]
    signal = indicator_and_signal[1]

    print("\nSYMBOL: " + query.symbol.upper())
    print("STRATEGY: {} ({}-day){}".format("Directional" if query.indicator[1] == "d" else "Simple moving average", query.indicator[0], ", buy above {}, sell \
below {}".format(_threshhold_to_string(the_indicator.buy_threshhold), _threshhold_to_string(the_indicator.sell_threshhold)) if query.indicator[1] == "d" else ""))
    print()
    print("{:15} {:15} {:15} {:15}".format("DATE", "CLOSE", "INDICATOR", "SIGNAL"))
    for i in range(len(stockList)):
        print("{0:15} {1:<15.2f} {2:<15{3}} {4:15}".format(stockList[i].date, float(stockList[i].close), stockList[i].indicator if stockList[i].indicator else "", ".2f" if type(stockList[i].indicator) == float else "", stockList[i].signal))

def _generateIndicatorAndSignal(query: QueryData) -> tuple:
    "Returns a tuple containing an indicator and signal in its two slots respectively, with their types based on the query data given by the user"
    if query.indicator[1] == "s":
        the_indicator = indicator.SimpleMovingAverageIndicator(query.indicator)
        signal = stock_signal.SimpleMovingAverageSignal()
    else:
        the_indicator = indicator.DirectionalIndicator(query.indicator)
        signal = stock_signal.DirectionalSignal()
    return the_indicator, signal

def _threshhold_to_string(threshhold: int):
    "Returns a string representation of a buy or sell threshhold, adding + if the threshhold is positive."
    return "+" + str(threshhold) if threshhold > 0 else str(threshhold)

def _promptUser() -> QueryData:
    "Prompts the user to enter data for which to search for."
    symbol = _promptForSymbol()
    dates = _promptForStartEnd()
    indicatorType = _promptForIndicatorType()
    return QueryData(symbol, dates[0], dates[1], indicatorType)

def _promptForIndicatorType() -> str:
    "Prompts the user to indicate which type of indicator they would like to use to analyze the stock prices."
    while True:
        indicator = input("What type of indicator would you like to use? ([S]imple moving average or [D]irectional): ").lower()
        if indicator == "s" or indicator == "d":
            break
        else:
            print("Invald input. Please choose S for simple moving average and D for directional indicator.\n")

    while True:
        try:
            days = int(input("Number of days for the indicator: "))
            if days <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Only numbers greater than zero are allowed. Please try again.")
    return days, indicator

def _promptForSymbol() -> str:
    "Prompt the user for the company's symbol or ticker for whch they would like to search"
    while True:
        symbol = input("Please enter the symbol for which you would like to search: ")
        try:
            with urllib.request.urlopen("http://ichart.yahoo.com/table.csv?s="+symbol) as response:
                break
        except HTTPError:
            print("Symbol invalid. Please try agin.")
    return symbol

def _promptForStartEnd() -> (datetime.date, datetime.date):
    "Prompt the user to input the start and end date for the period of stocks which they would like to analyze. Returns a tuple containing [0] - start date and [1] - end date"
    while True:
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        start_date_object = _parseAndCheckDateString(start_date)
        if not start_date_object:
            continue
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        end_date_object = _parseAndCheckDateString(end_date)
        if not end_date_object:
            continue
        today = datetime.date.today()

        if not (start_date_object and end_date_object):
            print("Please try again.\n")
        elif start_date_object > end_date_object:
            print("Your start date cannot be after your end date. Please try again.\n")
        elif start_date_object > today or end_date_object > today:
            print("Your dates cannot be after today's date. Please try again.\n")
        else:
            break
    return (_parseAndCheckDateString(start_date), _parseAndCheckDateString(end_date))

def _parseAndCheckDateString(date: str) -> bool or datetime.date:
    "Checks the date given to see if it is a valid date, raising an InvalidDateFormatError or ValueError if it is incorrect (incorrect format/invalid date). Returns a datetime.date object if no error encountered, else False"
    try:
        dateFormat = re.compile("^\d{4}-\d{2}-\d{2}$")
        if not dateFormat.match(date):
            raise InvalidDateFormatError(date)
        splitDate = date.split("-")
        theDate = datetime.date(int(splitDate[0]), int(splitDate[1]), int(splitDate[2]))
    except InvalidDateFormatError as e:
        print(e.msg)
    except ValueError: #raised by datetime.date when given something
        print("The date you entered is not in the calendar; it is an invalid date (e.g. xxxx-24-31).")
    else:
        return theDate

def _generate_closing_price_list(data_list: [tuple]) -> [float]:
    "Generate a list of closing prices based on a list of tuples that contain dates and closing prices"
    closing_prices = [float(price[1]) for price in data_list]
    return closing_prices

def _generate_date_list(data_list: [tuple]) -> [str]:
    "Generate a list of dates based on a list of tuples that contain dates and closing prices"
    dates = [date[0] for date in data_list]
    return dates

def _generate_stock_list(date_list, closing_price_list, indicator_and_signal) -> [Stock]:
    "Generate a list of stocks based on the date, closing price, indicator, and signal"
    the_indicator = indicator_and_signal[0]
    indicator_values = the_indicator.execute(closing_price_list)
    signal = indicator_and_signal[1]
    signal_values = signal.execute(closing_price_list, the_indicator)

    result = [Stock(date_list[i], closing_price_list[i], indicator_values[i], signal_values[i]) for i in range(len(closing_price_list))]
    return result

def run_interface():
    "Runs the user interface of the stocks program"
    query = _promptUser()
    url = connectToURL.queryURL(query)
    dates = _generate_date_list(connectToURL.download_data_from_url(url))
    closing_prices = _generate_closing_price_list(connectToURL.download_data_from_url(url))
    indicator_and_signal = _generateIndicatorAndSignal(query)

    stock_list = _generate_stock_list(dates, closing_prices, indicator_and_signal)
    _printChart(query, stock_list, indicator_and_signal)

if __name__ == "__main__":
    run_interface()
