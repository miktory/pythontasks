import csv
import os

def split_csv(filename):
    """Делит общую csv выгрузку на более мелкие выгрузки по годам.

        Args:
            filename (str): имя выгрузки
    """
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        if not os.path.exists("chunks"):
            os.makedirs("chunks")
        reader = csv.reader(file)
        header = next(reader)
        header_length = len(header)
        created_files = []
        for row in reader:
            if '' not in row and len(row) == header_length:
                vacancy = dict(zip(header, row))
                year = vacancy['published_at'][:4]
                file = open(f'chunks/{year}.csv', 'a', encoding='utf-8-sig', newline='')
                writer = csv.DictWriter(file, fieldnames=header)
                if year not in created_files:
                    created_files.append(year)
                    writer.writeheader()
                writer.writerow(vacancy)



