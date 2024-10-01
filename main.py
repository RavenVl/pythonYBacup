import yadisk
import os
import argparse
import zipfile
import loguru

from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
token = os.getenv('YANDEX_TOKEN')
y = yadisk.YaDisk(token=token)
parser = argparse.ArgumentParser(description='Backups files to YandexDisk')
parser.add_argument('-d' ,'--date' , action='store_true' , help='Backups files to YandexDisk by date')
logger = loguru.logger
logger.level("INFO")
logger.add("log_file.log", format="{time:DD-MM-YYYY HH:mm:ss} | {level} | {message}")
def run(path, dest_dir):
    """
    Загрузка папок и файлов
    :param path:
    """
    for address, dirs, files in os.walk(path):
        for dir in dirs:
            y.mkdir(f'/Резервные копии М2 Ардон-Фиш/{dest_dir}/{dir}')
            # print(f'Папка {dir} создана')
            # logger.info(f'Папка {dir} создана')
        for file in files:
            y.upload(f'{address}/{file}', f'/Резервные копии М2 Ардон-Фиш/{dest_dir}/{file}', overwrite=True, timeout=60)
            # logger.info(f'Файл {file} загружен')

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
            # print(f'Папка {dir} создана')
        with zipfile.ZipFile(f'{dest_dir}.zip', 'w') as zip:
            for file in files:
                zip.write(f'{address}/{file}')
                # logger.info(f'Файл {file} добавлен в архив')

        y.upload(f'{dest_dir}.zip', f'/Резервные копии М2 Ардон-Фиш/backup/{date}/{dest_dir}/{dest_dir}.zip',  overwrite=True, timeout=160)
        # print(f'Файл {dest_dir}.ziр загружен')
        logger.info(f'Файл {dest_dir}.ziр загружен')
        os.remove(f'{dest_dir}.zip')
def check():
    """
    Проверка токена!
    """
    print(y.check_token())

def main_run():
    args = parser.parse_args()

    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    if args.date:
        logger.info("Backup by date")
        check()
        run_date(r'd:\base_spu', 'base_spu', date)
        run_date(r'd:\base', 'base', date)
    else:
        logger.info("Backup by default")
        check()
        run(r'd:\base_spu', 'base_spu')
        run(r'd:\base', 'base')
    logger.info(f'Резервная копия М2 Ардон-Фиш создана: {date}')


if __name__ == '__main__':
    try:
        main_run()
    except Exception as e:
        logger.error(e)