import sys
import requests
import pandas as pd


@staticmethod
def get_currencies(filename):
    pd.set_option('expand_frame_repr', False)
    df = pd.read_csv(filename)
    sorted_currencies = df.groupby('salary_currency')['salary_currency'].count()
    sorted_currencies = sorted_currencies[sorted_currencies > 5000].to_dict()
    dates = []
    print('Частность, с которой встречаются валюты: ', sorted_currencies)
    sorted_currencies = list(sorted_currencies.keys())
    sorted_currencies.remove('RUR')
    date_sort = df.sort_values(by='published_at')['published_at']
    start_year = int(date_sort.iloc[1].split('-')[0])
    start_month = int(date_sort.iloc[1].split('-')[1])
    end_year = int(date_sort.iloc[-1].split('-')[0])
    end_month = int(date_sort.iloc[-1].split('-')[1])
    result_csv = pd.DataFrame(columns=['date'] + sorted_currencies)

    while start_year != end_year or start_month != end_month:
        if start_month in range(1, 10):
            dates.append('0{0}/{1}'.format(start_month, start_year))
        else:
            dates.append('{0}/{1}'.format(start_month, start_year))
        start_month += 1
        if start_month == 13:
            start_month = 1
            start_year += 1
    if start_month in range(1, 10):
        dates.append('0{0}/{1}'.format(start_month, start_year))
    else:
        dates.append('{0}/{1}'.format(start_month, start_year))
    print('Диапазон дат: ', dates[0], ' - ', dates[-1])

    for i, date in enumerate(dates):
        url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{date}d=1'
        response = requests.get(url)
        curr = pd.read_xml(response.text)
        curr_sort = curr.loc[curr['CharCode'].isin(sorted_currencies + ['BYN'])]
        month_currencies = {}
        for currency in sorted_currencies:
            value = 0
            if currency == "RUR":
                continue
            if currency == 'BYR' or currency == 'BYN':
                value = float(
                    curr_sort.loc[curr_sort['CharCode'].isin(['BYR', 'BYN'])]['Value'].values[0].replace(',', '.')) / \
                        (curr_sort.loc[curr_sort['CharCode'].isin(['BYR', 'BYN'])]['Nominal'].values[0])
                month_currencies[currency] = value
            else:
                value = float(curr_sort.loc[curr_sort['CharCode'] == currency]['Value'].values[0].replace(',', '.')) / \
                        (curr_sort.loc[curr_sort['CharCode'] == currency]['Nominal'].values[0])
                month_currencies[currency] = value
        date = date.split('/')
        result = [f'{date[1]}-{date[0]}']
        for key, value in month_currencies.items():
            result.append(month_currencies[key])
        result_csv.loc[i] = result

    result_csv.to_csv('currencies.csv')
    print(result_csv.head())
    print('Сохранено в файл currencies.csv')
    return result_csv
