import yadisk
import os
import argparse
import zipfile

from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
token = os.getenv('YANDEX_TOKEN')
y = yadisk.YaDisk(token=token)
parser = argparse.ArgumentParser(description='Backups files to YandexDisk')
parser.add_argument('-d' ,'--date' , action='store_true' , help='Backups files to YandexDisk by date')

def run(path, dest_dir):
    """
    Загрузка папок и файлов
    :param path:
    """
    for address, dirs, files in os.walk(path):
        for dir in dirs:
            y.mkdir(f'/Резервные копии М2 Ардон-Фиш/{dest_dir}/{dir}')
            print(f'Папка {dir} создана')
        for file in files:
            print(f'Файл {file} загружен')
            y.upload(f'{address}/{file}', f'/Резервные копии М2 Ардон-Фиш/{dest_dir}/{file}', overwrite=True, timeout=60)

def run_date(path,dest_dir, date):
    try:
        y.mkdir(f'/Резервные копии М2 Ардон-Фиш/backup/{date}')
    except yadisk.exceptions.DirectoryExistsError as e:
        pass
    try:
        y.mkdir(f'/Резервные копии М2 Ардон-Фиш/backup/{date}/{dest_dir}')
    except yadisk.exceptions.DirectoryExistsError as e:
        pass
    for address, dirs, files in os.walk(path):
        for dir in dirs:
            y.mkdir(f'/Резервные копии М2 Ардон-Фиш/backup/{date}/{dest_dir}/{dir}')
            print(f'Папка {dir} создана')
        with zipfile.ZipFile(f'{dest_dir}.zip', 'w') as zip:
            for file in files:
                print(f'Файл {file} загружен')
                zip.write(f'{address}/{file}')
        y.upload(f'{dest_dir}.zip', f'/Резервные копии М2 Ардон-Фиш/backup/{date}/{dest_dir}/{dest_dir}.zip',  overwrite=True, timeout=160)

def check():
    """
    Проверка токена!
    """
    print(y.check_token())

def main_run():
    args = parser.parse_args()
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    if args.date:
        print('Запуск по дате')
        check()
        run_date(r'd:\base_spu', 'base_spu', date)
        run_date(r'd:\base', 'base', date)
    else:
        print('Запуск по папкам')
        check()
        run(r'd:\base_spu', 'base_spu')
        run(r'd:\base', 'base')



if __name__ == '__main__':
    main_run()