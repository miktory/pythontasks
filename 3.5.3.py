import sqlite3
import pandas as pd
import sqlite3

filename = input("Введите название файла(vacancies_edited.db): ")
vacancy = input("Введите название профессии: ")
region = input("Введите название региона: ")
connect = sqlite3.connect(filename)
cur = connect.cursor()
years_salary = pd.read_sql(f"""SELECT SUBSTR(published_at, 1, 4) as 'Год',
         ROUND(AVG(salary)) as 'Средняя зарплата' from vacancies
        GROUP BY SUBSTR(published_at, 1, 4) """, connect)

years_count = pd.read_sql(f""" SELECT SUBSTR(published_at, 1, 4) as 'Год', COUNT(*) as 'Количество вакансий' from vacancies WHERE area_name == '{region}'
                            group by SUBSTR(published_at, 1, 4) """, connect)

years_salary_vac = pd.read_sql(f"""SELECT SUBSTR(published_at, 1, 4) as 'Год',
                                                    ROUND(AVG(salary), 2) as 'Средняя зарплата - {vacancy}'
                                                    from vacancies 
                                                    where lower(name) LIKE '%{vacancy.lower()}%' and area_name == '{region}'
                                                    group by SUBSTR(published_at, 1, 4) """, connect)

years_count_vac = pd.read_sql(f"""SELECT SUBSTR(published_at, 1, 4) as 'Год',
                                                    COUNT(*) as 'Количество вакансий - {vacancy}'
                                                    from vacancies 
                                                    where lower(name) LIKE '%{vacancy.lower()}%' and area_name == '{region}'
                                                    group by SUBSTR(published_at, 1, 4) """, connect)

area_salary = pd.read_sql("""SELECT area_name as 'Город',  ROUND(AVG(salary), 2) as 'Средняя зарплата'
                                         from vacancies 
                                         group by area_name
                                         having COUNT(*) >= (SELECT COUNT(*) FROM vacancies) / 100
                                         ORDER BY ROUND(AVG(salary), 2) DESC 
                                         LIMIT 10""", connect)

area_percentage = pd.read_sql("""SELECT area_name as 'Город',
                                                100 * COUNT(*)/(select COUNT(*) from vacancies)  as 'Доля вакансий (%)'
                                                from vacancies
                                                group by area_name
                                                having COUNT(*) >= (SELECT COUNT(*) FROM vacancies) / 100
                                                ORDER BY COUNT(*) DESC 
                                                LIMIT 10""", connect)

print('Динамика уровня зарплат по годам в указанном регионе: \n', years_salary, '\n')
print('Динамика количества вакансий по годам в указанном регионе: \n', years_count, '\n')
print('Динамика уровня зарплат по годам для выбранной профессии в указанном регионе: \n', years_salary_vac, '\n')
print('Динамика количества вакансий по годам для выбранной профессии в указанном регионе: \n', years_count_vac,'\n')
print('Уровень зарплат по городам (в порядке убывания): \n', area_salary, '\n')
print('Доля вакансий по городам (в порядке убывания): \n', area_percentage, '\n')