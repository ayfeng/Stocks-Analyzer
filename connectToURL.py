import urllib.request
from interface import QueryData

def queryURL(query_data: QueryData) -> str:
    "Generates a URL based on the QueryData object which contains a company's symbol, starting date, ending date, and indicator type/number of days"
    return "http://ichart.yahoo.com/table.csv?s={}&a={}&b={}&c={}&d={}&e={}&f={}&g=d".format(query_data.symbol, query_data.start.month-1, query_data.start.day, query_data.start.year ,query_data.end.month-1, query_data.end.day, query_data.end.year)

def download_data_from_url(url: str):
    "Attempts to access a URL. Returns a list of tuples whose first element is the date and second element is the closing price"
    response = None
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))
    else:
        data = response.read()
        string_data = data.decode(encoding = "utf-8").splitlines()
        result = []
        for i in string_data[1:]:
            splitted_line = i.split(",")
            result.append((splitted_line[0], float(splitted_line[4])))
    finally:
        if response != None:
            response.close()
    return result
