import sqlite3
import pandas as pd
from statistics import mean
import math


def edit_salary(date, salary_from, salary_to, salary_currency, cursor):
    currency = 0
    if salary_currency in ['BYN', 'BYR', 'EUR', 'KZT', 'UAH', 'USD']:
        salary_currency.replace('BYN', 'BYR')
        currency = cursor.execute("select * from currencies where date == :published",
                                           {"published": f"{date[0]}-{date[1]}"}).fetchone()[
            currencies_num[salary_currency]]
    elif salary_currency == 'RUR':
        currency = 1
    if math.isnan(salary_to) or math.isnan(salary_from):
        salary = salary_to if math.isnan(salary_from) else salary_from
    else:
        salary = math.floor((salary_from + salary_to) / 2)
    if math.isnan(salary):
        return 0

    return math.floor(float(salary) * float(currency))


currencies_num = {"BYR": 2, "USD": 6, "EUR": 3, "KZT": 4, "UAH": 5}
connection = sqlite3.connect("currencies.db")
pd.set_option("expand_frame_repr", False)
df = pd.read_csv(input("Введите имя файла (vacancies_dif_currencies.csv): "))
cursor = connection.cursor()
df["salary"] = df.apply(lambda x: edit_salary(x["published_at"][:7].split("-"), x["salary_from"], x["salary_to"], x["salary_currency"], cursor), axis=1)
df["published_at"] = df.apply(lambda x: x["published_at"][0:7], axis=1)
df = df.drop(["salary_from", "salary_to", "salary_currency"], axis=1)
df = df.loc[:, ["name", "salary", "area_name", "published_at"]]
df = df[df.salary > 0]
connection.close()
connection = sqlite3.connect("vacancies_edited.db")
df.to_sql("vacancies", con=connection, if_exists="replace", index=False)
connection.commit()
connection.close()
print("Обработанный файл сохранён под названием vacancies_edited.db")