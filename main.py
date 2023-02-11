import requests
import configparser as cf # Для парса конфига
import os, json, shutil, sys
from pprint import pprint
from progress.bar import IncrementalBar
from ya_metods import * # Там код для работы с диском

config = cf.ConfigParser()
config.read("config.ini")
disk_token = config.get('TOKEN','disk_token') # Токен диска
serv_key = config.get('TOKEN','serv_key') # Сервисный ключ доступа 🤖

# Проверим введение данных в конфиге
if disk_token == 'your token':
    print('Вы не ввели токен в конфиг!')
    sys.exit()
elif serv_key == 'your key':
    print('Вы не ввели ключ в конфиг!')
    sys.exit()

own_id = input('Введите id пользователя ВКонтакте: |')

# Очистим папку
try:
    os.makedirs('saved_pictures/piks_out')
except FileExistsError:
    print('')
shutil.rmtree('saved_pictures/piks_out')
os.makedirs('saved_pictures/piks_out')

bar = IncrementalBar('Скачивание с ВК:', max = 6) 

bar.next()
URL = 'https://api.vk.com/method/photos.get' 
params = {
    'access_token': serv_key,
    'owner_id':own_id,
    'album_id':'profile',
    'v':'5.131',
    'extended':'1'
}

bar.next()

res = requests.get(URL, params=params) # Пускаем запрос 🚀

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

# Проверим наличие фото
if len(new_json) == 0:
    print('\nНа странице нет фотографий профиля!')
    sys.exit()

bar.next()

json_save = []
for image in new_json:
    img_dict = {}
    img_dict["file_name"] = f'{image}.jpg'
    img_dict["size"] = 'z'
    json_save.append(img_dict)

with open('saved_pictures/saved_pics.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json.dumps(json_save, indent=2, ensure_ascii=False))

bar.next()
bar.finish()

# Полетели на диск

bar = IncrementalBar('Загрузка на диск:', max = 3 + len(new_json)*2)
ya = YandexDisk(disk_token)
ya.create_folder('VK photos') # создаём папку для выгрузки

bar.next()

for image in new_json: # Скачаем фотографии
    img_data = requests.get(new_json.get(image)).content
    with open(f'saved_pictures/piks_out/{image}.jpg', 'wb') as handler:
        handler.write(img_data)
    bar.next()

bar.next()

for image in new_json: # Отправим на диск 👾
    try:
        ya.upload_photo(f'VK photos/{image}', f'saved_pictures/piks_out/{image}.jpg')
        bar.next()
    except requests.exceptions.HTTPError:
        print('\nФото не найдено! Возможно оно не существует. Проверьте ссылку', new_json.get(image))
        bar.next()
        continue
bar.next()
bar.finish()

print('\nЗагрузка выполнена успешно!')