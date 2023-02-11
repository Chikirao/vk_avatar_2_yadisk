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
        return response.json()
    

# ya = YandexDisk(disk_token)
# ya.create_folder('VK photos')