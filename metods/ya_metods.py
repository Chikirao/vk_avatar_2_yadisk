import requests
from pprint import pprint
import configparser as cf

config = cf.ConfigParser()
config.read("config2.ini")
disk_token = config.get('TOKEN','disk_token') # Токен диска

class YandexDisk:

    def __init__(self, token):
        self.token = token
    
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
    
    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()
    
    def create_folder(self, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {"path": path}
        response = requests.put(url, headers=headers, params=params)
        if response.status_code == 201:
            print(' Папка создана!')
        elif response.status_code == 400:
            print(' Ошибка 400! Некорректные данные.')
        elif response.status_code == 413:
            print(' Загрузка файла недоступна. Файл слишком большой.')
        elif response.status_code == 423:
            print(' Технические работы. Сейчас можно только просматривать и скачивать файлы.')
        elif response.status_code == 429:
            print(' Слишком много запросов! Попробуйте позже.')
        elif response.status_code == 503:
            print(' Сервис временно недоступен.')
        elif response.status_code == 507:
            print(' Недостаточно свободного места.')
        else:
            (' Неизвестная ошибка')
        return response.json()
    
    def upload_photo(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        try:
            response = requests.put(href, data=open(filename, 'rb'))
        except requests.exceptions.MissingSchema:
            print("\nНеизвестная ошибка!")
        response.raise_for_status()
        if response.status_code == 201:
            print(' Фото загружено!')
        elif response.status_code == 400:
            print(' Ошибка 400! Некорректные данные.')
        elif response.status_code == 413:
            print(' Загрузка файла недоступна. Файл слишком большой.')
        elif response.status_code == 423:
            print(' Технические работы. Сейчас можно только просматривать и скачивать файлы.')
        elif response.status_code == 429:
            print(' Слишком много запросов! Попробуйте позже.')
        elif response.status_code == 503:
            print(' Сервис временно недоступен.')
        elif response.status_code == 507:
            print(' Недостаточно свободного места.')
        else:
            (' Неизвестная ошибка')