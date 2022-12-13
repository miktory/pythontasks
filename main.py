from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side
from openpyxl.styles.numbers import FORMAT_PERCENTAGE_00
from openpyxl.utils import get_column_letter
import pdfkit
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
import numpy as np
from inform import display, Error
from vdiff import Vdiff

def as_text(value):
    if value is None:
        return ""
    return str(value)


years_salary_dic = {2007: 38916, 2008: 43646, 2009: 42492, 2010: 43846, 2011: 47451, 2012: 48243, 2013: 51510,
                    2014: 50658, 2015: 52696, 2016: 62675, 2017: 60935, 2018: 58335, 2019: 69467, 2020: 73431,
                    2021: 82690, 2022: 91795}
years_count_dic = {2007: 2196, 2008: 17549, 2009: 17709, 2010: 29093, 2011: 36700, 2012: 44153, 2013: 59954,
                   2014: 66837, 2015: 70039, 2016: 75145, 2017: 82823, 2018: 131701, 2019: 115086, 2020: 102243,
                   2021: 57623, 2022: 18294}
years_salary_vac_dic = {2007: 43770, 2008: 50412, 2009: 46699, 2010: 50570, 2011: 55770, 2012: 57960,
                        2013: 58804, 2014: 62384, 2015: 62322, 2016: 66817, 2017: 72460, 2018: 76879,
                        2019: 85300, 2020: 89791, 2021: 100987, 2022: 116651}
years_count_vac_dic = {2007: 317, 2008: 2460, 2009: 2066, 2010: 3614, 2011: 4422, 2012: 4966, 2013: 5990,
                       2014: 5492, 2015: 5375, 2016: 7219, 2017: 8105, 2018: 10062, 2019: 9016, 2020: 7113,
                       2021: 3466, 2022: 1115}
area_salary_dic = {'Москва': 76970, 'Санкт-Петербург': 65286, 'Новосибирск': 62254, 'Екатеринбург': 60962,
                   'Казань': 52580, 'Краснодар': 51644, 'Челябинск': 51265, 'Самара': 50994, 'Пермь': 48089,
                   'Нижний Новгород': 47662}
area_count_dic = {'Москва': 0.3246, 'Санкт-Петербург': 0.1197, 'Новосибирск': 0.0271, 'Казань': 0.0237,
                  'Нижний Новгород': 0.0232, 'Ростов-на-Дону': 0.0209, 'Екатеринбург': 0.0207,
                  'Краснодар': 0.0185, 'Самара': 0.0143, 'Воронеж': 0.0141}

years_salary_dic = {2007: 38916, 2008: 43646, 2009: 42492, 2010: 43846, 2011: 47451, 2012: 48243, 2013: 51510,
                    2014: 50658}
years_count_dic = {2007: 2196, 2008: 17549, 2009: 17709, 2010: 29093, 2011: 36700, 2012: 44153, 2013: 59954,
                   2014: 66837}
years_salary_vac_dic = {2007: 43770, 2008: 50412, 2009: 46699, 2010: 50570, 2011: 55770, 2012: 57960, 2013: 58804,
                        2014: 62384}
years_count_vac_dic = {2007: 317, 2008: 2460, 2009: 2066, 2010: 3614, 2011: 4422, 2012: 4966, 2013: 5990, 2014: 5492}
area_salary_dic = {'Москва': 57354, 'Санкт-Петербург': 46291, 'Новосибирск': 41580, 'Екатеринбург': 41091,
                   'Казань': 37587, 'Самара': 34091, 'Нижний Новгород': 33637, 'Ярославль': 32744, 'Краснодар': 32542,
                   'Воронеж': 29725}
area_count_dic = {'Москва': 0.4581, 'Санкт-Петербург': 0.1415, 'Нижний Новгород': 0.0269, 'Казань': 0.0266,
                  'Ростов-на-Дону': 0.0234, 'Новосибирск': 0.0202, 'Екатеринбург': 0.0143, 'Воронеж': 0.014,
                  'Самара': 0.0133, 'Краснодар': 0.0131}
first_sheet_data = [years_salary_dic, years_salary_vac_dic, years_count_dic, years_count_vac_dic]
first_table_data = [years_salary_dic, years_salary_vac_dic, years_count_dic, years_count_vac_dic]
second_sheet_data = [area_salary_dic,area_count_dic]


class Report:
    def generate_excel(self, data1, column_names, column_names2, data2):
        def auto_width(sheets):
            for sheet in sheets:
                for sheet_column_cells in sheet.columns:
                    new_column_length = max(len(str(cell.value)) for cell in sheet_column_cells)
                    new_column_letter = (get_column_letter(sheet_column_cells[0].column))
                    if new_column_length > 0:
                        sheet.column_dimensions[new_column_letter].width = new_column_length * 1.23

        wb = Workbook()
        ws = wb.active
        ws1 = wb.create_sheet("Статистика по городам")
        ws.title = 'Статистика по годам'
        border_style = Side(border_style="thin", color="000000")
        border = Border(top=border_style, left=border_style, right=border_style, bottom=border_style)
        # Первый лист
        for i in range(len(column_names)):
            cell = ws.cell(row=1, column=i + 1, value=column_names[i])
            cell.font = Font(bold=True)
        for i, key in enumerate(data1[0]):
            ws.cell(row=i + 2, column=1, value=key)
            ws.cell(row=i + 2, column=2, value=data1[0][key])
            ws.cell(row=i + 2, column=3, value=data1[1][key])
            ws.cell(row=i + 2, column=4, value=data1[2][key])
            ws.cell(row=i + 2, column=5, value=data1[3][key])
        for column_cells in ws.columns:
            for cell in column_cells:
                cell.border = border
        # Второй лист
        lst = []
        lst.append(ws1.cell(row=1, column=1, value=column_names2[0]))
        lst.append(ws1.cell(row=1, column=2, value=column_names2[1]))
        lst.append(ws1.cell(row=1, column=4, value=column_names2[2]))
        lst.append(ws1.cell(row=1, column=5, value=column_names2[3]))
        for cell in lst:
            cell.font = Font(bold=True)
            cell.border = border
        for i, key in enumerate(data2[0]):
            ws1.cell(row=i+2, column=1, value=key)
            ws1.cell(row=i + 2, column=2, value=data2[0][key])
        for i, key in enumerate(data2[1]):
            ws1.cell(row=i+2, column=4, value=key)
            ws1.cell(row=i + 2, column=5, value=str('%.2f' % round(data2[1][key]*100, 2))+'%').number_format = '0.00%'
        for column_cells in ws1.columns:
            for cell in column_cells:
                if cell.column!=3:
                    cell.border = border
        auto_width([ws,ws1])
        wb.save('report.xlsx')

    def generate_image(self, data1, profession_name, data2, data3, data4):
        fig,axs = plt.subplots(2, 2)
        #Первый график
        width = 0.4
        plt.rcParams.update({'font.size': 8})
        axs[0, 0].bar([x - width * 0.5 for x in list(data1[0].keys())], data1[0].values(), width, label='средняя з/п')
        axs[0, 0].bar([x + width * 0.5 for x in list(data1[1].keys())], data1[1].values(), width,
                label=f'з/п {profession_name}')
        axs[0, 0].legend()
        axs[0, 0].set_title("Уровень зарплат по годам", fontsize=12)
        axs[0, 0].grid(axis='y')
        plt.sca(axs[0, 0])
        plt.xticks(np.arange(min(list(data1[0].keys())), max(list(data1[0].keys()))+1, 1.0),rotation=90)
        # Второй график
        axs[0, 1].bar([x - width * 0.5 for x in list(data2[0].keys())], data2[0].values(), width,
                 label='Количество вакансий')
        axs[0, 1].bar([x + width * 0.5 for x in list(data2[1].keys())], data2[1].values(), width,
                 label=f'Количество вакансий \n{profession_name}')
        axs[0, 1].grid(axis='y')
        plt.sca(axs[0, 1])
        plt.xticks(np.arange(min(list(data1[1].keys())), max(list(data1[1].keys()))+1, 1.0), rotation=90)
        axs[0, 1].legend()
        axs[0, 1].set_title('Количество вакансий по годам', fontsize=12)
        # Третий график
        width = 0.8
        keys = list(data3.keys())
        for i, key in enumerate(keys):
            keys[i] = keys[i].replace(" ", '\n')
            keys[i] = keys[i].replace('-', '-\n')
        keys.reverse()
        values = list(data3.values())
        values.reverse()
        axs[1, 0].barh(keys, values, width, label='Количество вакансий')
        axs[1, 0].set_title('Уровень зарплат по городам', fontsize=12)
        axs[1, 0].grid(axis='x')
        plt.sca(axs[1, 0])
        plt.yticks(fontsize=6)
        plt.xticks(np.arange(0, max(values) + 20000, 20000))
        # Четвёртый график
        share = 1
        for key in data4:
            share -= data4[key]
        data4['Другие'] = share
        axs[1, 1].pie(data4.values(), labels=data4.keys(), startangle=450, textprops={'fontsize': 6})
        axs[1, 1].set_title('Доля вакансий по городам', fontsize=12)
        # Вывод графика и сохранение в .png
        fig.tight_layout()
        plt.show()
        fig.savefig('graph.png')

    def generate_pdf(self,profession_name, data1, column_names1, data2, column_names2, data3, column_names3):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("pdf_template.html")
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        table1_columns = ""
        table1_rows = ""
        table2_columns = ""
        table2_rows = ""
        table3_columns = ""
        table3_rows = ""
        for i in range(0,len(column_names1)):
            table1_columns += '<th>' + column_names1[i] + '</th>'
        for i in range(0, len(data1[0])):
            table1_rows += '<tr>' + f'<td>{list(data1[0].keys())[i]}</td>' + f'<td><center>{list(data1[0].values())[i]}</center></td>' + \
                           f'<td><center>{list(data1[1].values())[i]}</center></td>' + f'<td><center>{list(data1[2].values())[i]}</center></td>' + \
                           f'<td><center>{list(data1[3].values())[i]}</center></td>' + '</tr>'
        for i in range(0, len(column_names2)):
            table2_columns += '<th>' + column_names2[i] + '</th>'
        for i in range(0, len(data2)):
            table2_rows += '<tr>' + f'<td><center>{list(data2.keys())[i]}</center></td>' + f'<td><center>{list(data2.values())[i]}</center></td>' + '</tr>'
        for i in range(0, len(column_names3)):
            table3_columns += '<th>' + column_names3[i] + '</th>'
        for i in range(0, len(data3)):
            table3_rows += '<tr>' + f'<td><center>{list(data3.keys())[i]}</center></td>' + f'<td><center>{list(data3.values())[i]}</center></td>' + '</tr>'
        pdf_template = template.render({'profession_name': profession_name, 'image_path':'file:///C:/Users/Матвей/PycharmProjects/statistics/graph.png',
                                        'table1_columns':table1_columns, 'table1_rows':table1_rows, 'table2_columns':table2_columns, 'table2_rows':table2_rows,
                                        'table3_columns':table3_columns, 'table3_rows':table3_rows})
        pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options={"enable-local-file-access": ""})

    def print_report(self, years_salary, years_count, years_salary_vac, years_count_vac, area_salary, area_count):
        print("Динамика уровня зарплат по годам: " + str(years_salary))
        print("Динамика количества вакансий по годам: " + str(years_count))
        print("Динамика уровня зарплат по годам для выбранной профессии: " + str(years_salary_vac))
        print("Динамика количества вакансий по годам для выбранной профессии: " + str(years_count_vac))
        print("Уровень зарплат по городам (в порядке убывания): " + str(area_salary))
        print("Доля вакансий по городам (в порядке убывания): " + str(area_count))

report = Report()
program_action = input('Введите данные для печати: ')
if program_action == 'Вакансии':
    report.print_report(years_salary_dic, years_count_dic, years_salary_vac_dic,years_count_vac_dic, area_salary_dic, area_count_dic)
elif program_action == 'Статистика':
    report = Report()
    report.generate_excel(first_sheet_data,
                      ['Год', 'Средняя зарплата', 'Средняя зарплата - Программист', 'Количество вакансий',
                       'Количество вакансия - Программист'], ['Город', 'Уровень зарплат', 'Город', 'Доля вакансий'],second_sheet_data)
    report.generate_image([years_salary_dic, years_salary_vac_dic], 'программист', [years_count_dic, years_count_vac_dic]
                      , area_salary_dic, area_count_dic)
    table3_data = {}
    for i in range(0, len(area_count_dic)-1):
        value = str('%.2f' % round(list(area_count_dic.values())[i]*100, 2)+'%')
        table3_data[list(area_count_dic.keys())[i]] = value
    report.generate_pdf('Программист',first_table_data,['Год', 'Средняя зарплата', 'Средняя зарплата - Программист', 'Количество вакансий',
                        'Количество вакансий - Программист'],area_salary_dic,['Город', 'Уровень зарплат'],table3_data,['Город', 'Доля вакансий'])
    print('asdf')
