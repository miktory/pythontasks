import requests
import time
from datetime import datetime
import pandas as pd
from datetime import datetime as dt

pd.set_option('expand_frame_repr', False)
today = input('Введите дату в следующем формате (2022-12-01 22:00:00): ')
today = dt.strptime(today,'%Y-%m-%d %H:%M:%S')
urls = []
for day in range(1, today.day + 1):
    for hour in range(0, 24, 2):
        if today.replace(day=day).weekday() not in [5, 6]:
            end = f'{format((hour + 2), "02d")}:00:00'
            if hour == 22:
                end = '23:59:59'
            urls.append(f'https://api.hh.ru/vacancies?date_from=2022-{today.month}-{format(day, "02d")}T{format(hour, "02d")}:00:00&'
                         f'date_to=2022-{today.month}-{format(day, "02d")}T{end}&specialization=1&per_page=100')
df = pd.DataFrame(columns=["name", "salary_from", "salary_to", "salary_currency", "area_name", "published_at"])
for url in urls:
    pages = requests.get(url).json()['pages']
    time.sleep(5)
    for page in range(pages):
        response = requests.get(url, params={'page': page})
        vacancies = response.json()
        for vacancy in vacancies['items']:
            try:
                df.loc[len(df)] = [vacancy["name"], vacancy["salary"]["from"], vacancy["salary"]["to"], vacancy["salary"]["currency"], vacancy["area"]["name"], vacancy["published_at"]]
            except Exception:
                continue
df.to_csv('HH_vacancies.csv', index=False)
print(df.head(1000))