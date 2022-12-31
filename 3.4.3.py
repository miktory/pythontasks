import math
import os
import shutil
import pandas as pd
from main import Report
from multiprocessing import Process, Queue

pd.options.mode.chained_assignment = None


class Results:
    def __init__(self):
        self.years_count = {}
        self.years_salary = {}
        self.years_count_vac = {}
        self.years_salary_vac = {}
        self.area_count = {}
        self.area_salary = {}


class UserInput:
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.vacancy = input('Введите название профессии: ')
        self.region = input('Укажите регион: ')


def get_salary(x, currencies):
    salary_from, salary_to, salary_currency, published_at = x.loc['salary_from'], x.loc['salary_to'], x.loc[
        'salary_currency'], x.loc['published_at']
    currencies_to_work = list(currencies.loc[:, ~currencies.columns.isin(['date'])].columns.values)
    date = published_at[:7]
    if math.isnan(salary_to) or math.isnan(salary_from):
        salary = salary_to if math.isnan(salary_from) else salary_from
    else:
        salary = math.floor((salary_from + salary_to) / 2)
    if salary_currency == 'RUR' or salary_currency not in currencies_to_work:
        return salary
    return math.floor(salary * currencies.loc[currencies['date'] == date][salary_currency].values[0])


def get_year_statistics(file_name, vacancy, q, currencies, region):
    df = pd.read_csv(file_name)
    df = fill_dataframe(df, currencies)
    data_job = df[df['name'].str.contains(vacancy, case=False)]
    data_job = data_job[data_job['area_name'].str.contains(region, case=False)]
    q.put([int(df['published_at'].values[0][:4]), df.shape[0], math.floor(df['salary'].mean()), data_job.shape[0],
           math.floor(data_job['salary'].mean()), df])


def fill_dataframe(df, currencies):
    cr = list(currencies.loc[:, ~currencies.columns.isin(['date'])].columns.values) + ['RUR']
    df = df[df['salary_currency'].isin(cr)]
    df['salary'] = df.apply(lambda x: get_salary(x, currencies), axis=1)
    df.drop(columns=['salary_from', 'salary_to', 'salary_currency'], inplace=True)
    df = df.reindex(columns=['name', 'salary', 'area_name', 'published_at'], copy=True)
    return df


def get_all_years_statistics():
    global st, df_res
    process = []
    q = Queue()
    currencies = pd.read_csv('currencies.csv')
    for file_name in os.listdir(temp):
        p = Process(target=get_year_statistics, args=(temp + '/' + file_name, user_input.vacancy, q, currencies.copy(), user_input.region))
        process.append(p)
        p.start()
    for p in process:
        p.join(1)
        data = q.get()
        st.years_count[data[0]] = data[1]
        st.years_salary[data[0]] = data[2]
        st.years_count_vac[data[0]] = data[3]
        st.years_salary_vac[data[0]] = data[4]
        df_res.append(data[5])
    st.years_count = dict(sorted(st.years_count.items(), key=lambda i: i[0]))
    st.years_salary = dict(sorted(st.years_salary.items(), key=lambda i: i[0]))
    st.years_count_vac = dict(sorted(st.years_count_vac.items(), key=lambda i: i[0]))
    st.years_salary_vac = dict(sorted(st.years_salary_vac.items(), key=lambda i: i[0]))


def calc_area_stats():
    global st
    df = pd.concat(df_res, ignore_index=True)
    all_vac_num = df.shape[0]
    vac_percent = int(all_vac_num * 0.01)

    data = df.groupby('area_name')['name'] \
        .count() \
        .apply(lambda x: round(x / all_vac_num, 4)) \
        .sort_values(ascending=False) \
        .head(10) \
        .to_dict()
    st.area_count = data

    area_vac_num = df.groupby('area_name')['name'] \
        .count() \
        .loc[lambda x: x > vac_percent] \
        .to_dict()

    data = df.loc[df['area_name'].isin(area_vac_num.keys())] \
        .groupby('area_name')['salary'] \
        .mean() \
        .apply(lambda x: math.floor(x)) \
        .sort_values(ascending=False) \
        .head(10) \
        .to_dict()
    st.area_salary = data


def get_stats():
  #  print(f'Динамика уровня зарплат по годам: {st.years_salary}')
  #  print(f'Динамика количества вакансий по годам: {st.years_count}')
    print(f'Динамика уровня зарплат по годам для выбранной профессии: {st.years_salary_vac}')
    print(f'Динамика количества вакансий по годам для выбранной профессии: {st.years_count_vac}')
    print(f'Уровень зарплат по городам (в порядке убывания): {st.area_salary}')
    print(f'Доля вакансий по городам (в порядке убывания): {st.area_count}')


if __name__ == '__main__':
    st = Results()
    df_res = []
    temp = 'temp'
    user_input = UserInput()
    new_path = fr'./{temp}'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    df = pd.read_csv(user_input.file_name)
    df['year'] = df['published_at'].apply(lambda x: x[0:4])
    df_group = df.groupby('year')
    for year, data in df_group:
        data.loc[:, data.columns != 'year'].to_csv(rf'{new_path}\{year}.csv', index=False)
    get_all_years_statistics()
    calc_area_stats()
    get_stats()
    first_sheet_data = [st.years_salary, st.years_salary_vac, st.years_count,
                        st.years_count_vac]

    second_sheet_data = [st.area_salary, st.area_count]
    Report.generate_excel(first_sheet_data,
                          ['Год', 'Средняя зарплата', 'Средняя зарплата - {0}'.format(user_input.vacancy),
                           'Количество вакансий',
                           'Количество вакансий - {0}'.format(user_input.vacancy)],
                          ['Город', 'Уровень зарплат', 'Город', 'Доля вакансий'], second_sheet_data)
    image_empty_data1= st.years_salary.copy()
    for key,value in image_empty_data1.items():
        image_empty_data1[key] = 0
    image_empty_data2 = st.years_count.copy()
    for key, value in image_empty_data2.items():
        image_empty_data2[key] = 0
    Report.generate_image([image_empty_data1, st.years_salary_vac], user_input.vacancy,
                          [image_empty_data2, st.years_count_vac]
                          , st.area_salary, st.area_count)
    table3_data = {}
    for i in range(0, len(st.area_count) - 1):
        value = str('%.2f' % round(list(st.area_count.values())[i] * 100, 2) + '%')
        table3_data[list(st.area_salary.keys())[i]] = value
    for key, value in image_empty_data1.items():
        image_empty_data1[key] = " "
    image_empty_data2 = st.years_count.copy()
    for key, value in image_empty_data2.items():
        image_empty_data2[key] = " "
    first_table_data = [image_empty_data1, st.years_salary_vac, image_empty_data2,
                        st.years_count_vac]
    Report.generate_pdf(user_input.vacancy, first_table_data,
                        ['Год', ' ', 'Средняя зарплата - {0} в г.{1}'.format(user_input.vacancy, user_input.region),
                         ' ', 'Количество вакансий - {0} в г.{1}'.format(user_input.vacancy, user_input.region)],
                        st.area_salary, ['Город', 'Уровень зарплат'], table3_data,
                        ['Город', 'Доля вакансий'])
    shutil.rmtree(rf'./{temp}')
    print('Отчёт сгенерирован и сохранён в report.pdf')

