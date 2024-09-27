import yadisk
import os

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('YANDEX_TOKEN')
y = yadisk.YaDisk(token=token)


def run(path):
    """
    Загрузка папок и файлов
    :param path:
    """
    for address, dirs, files in os.walk(path):
        for dir in dirs:
            y.mkdir(f'/Резервные копии М2 Ардон-Фиш/{dir}')
            print(f'Папка {dir} создана')
        for file in files:
            print(f'Файл {file} загружен')
            y.upload(f'{address}/{file}', f'/Резервные копии М2 Ардон-Фиш/{file}')


def check():
    """
    Проверка токена
    """
    print(y.check_token())


if __name__ == '__main__':
    # run(r'c:\Users\raven\YandexDisk\Загрузки\book\new')
    check()
