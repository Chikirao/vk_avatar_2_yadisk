import requests
import configparser as cf # Для парса конфига
import time, vk, os, json
from pprint import pprint
from progress.bar import IncrementalBar
from ya_metods import * # Там код для работы с диском

bar = IncrementalBar('Скачивание с ВК:', max = 6) 

config = cf.ConfigParser()
config.read("config2.ini")
disk_token = config.get('TOKEN','disk_token') # Токен диска

vk_token = config.get('TOKEN', 'vk_access_token') # Токен и id вк (не обязательно)
vk_id = str(config.get('TOKEN', 'vk_user_id'))

serv_key = 'c3d398bec3d398bec3d398be24c0c11502cc3d3c3d398bea0306811fe8afcb75ebc4ae9' # Сервисный ключ доступа
bar.next()
URL = 'https://api.vk.com/method/photos.get' 
params = {
    'access_token': serv_key,
    'owner_id':'1',
    'album_id':'profile',
    'v':'5.131',
    'extended':'1'
}

bar.next()

res = requests.get(URL, params=params) # Пускаем запрос 🚀
# pprint(res.json())

bar.next()

with open('pics.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json.dumps(res.json(), indent=2, ensure_ascii=False))

bar.next()

# Запишем новый json с получеными фото
new_json = {}
for photo in res.json()["response"]["items"]:
    for size in photo.get("sizes"):
        if size.get("type") == "z":
            new_json[f'{photo.get("likes").get("count")}_{photo.get("date")}'] = size.get("url")

bar.next()

with open('saved_pictures/saved_pics.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json.dumps(new_json, indent=2, ensure_ascii=False))
# print(new_json)

bar.next()
bar.finish()

# Полетели на диск

bar = IncrementalBar('Загрузка на диск:', max = 6)
ya = YandexDisk(disk_token)
ya.create_folder('VK photos') # создаём папку для выгрузки

bar.next()
