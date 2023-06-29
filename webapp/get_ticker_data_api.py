import requests
import csv
from secrets import *
import tempfile 

# def get_temp_csv(ticker):
#     temp_csv = f'temp_{ticker}.csv'
#     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={ticker}&interval=30min&slice=year1month1&adjusted=false&apikey=GQETSN88IK9K35EH'
#     with requests.Session() as s:
#         download = s.get(url)
#         decoded_content = download.content .decode('utf-8')
#         cr = csv.reader(decoded_content.splitlines(), delimiter=',')
#         my_list = list(cr)
#     with open(temp_csv, 'a', newline='') as f:
#         writer = csv.writer(f)
#         for row in my_list:
#             writer.writerow(row)
#     f.close()


def get_temp_csv(ticker, api_key):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={ticker}&interval=30min&slice=year1month1&adjusted=false&apikey={api_key}'
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
        writer = csv.writer(temp_file)
        for row in my_list:
            writer.writerow(row)
        temp_csv = temp_file.name

    return temp_csv