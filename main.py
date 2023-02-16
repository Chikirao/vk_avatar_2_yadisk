import requests
import configparser as cf # Для парса конфига
import os, json, shutil, sys
from pprint import pprint
from progress.bar import IncrementalBar
from metods.ya_metods import * # Там код для работы с диском
from metods.vk_metods import * # Там код для работы с вк

config = cf.ConfigParser()
config.read("config.ini")
serv_key = config.get('TOKEN','serv_key') # Сервисный ключ доступа 🤖

if serv_key == 'your key':
    print('Вставьте свой сервисный ключ ВК АПИ в файл config.ini!')

from_album = input('Из какого альбома будем получать фотографии?(wall - фото со стены, profile - аватарка профиля, a - отдельное id фльбома.)\nНапишите w/p/a :|')
if from_album not in ['w', 'p', 'a', 'W', 'P', 'A']:
    print('Не верная команда!')
    sys.exit()
disk_token = input('Введите ваш токен от Яндекс Диска: |')
own_id = input('Введите id пользователя ВКонтакте: |')
fold_name = input('Название создаваемой папки на диске: |')

# Очистим папку
try: os.makedirs('saved_pictures/piks_out')
except FileExistsError: print('')
shutil.rmtree('saved_pictures/piks_out')
os.makedirs('saved_pictures/piks_out')

bar = IncrementalBar('Скачивание с ВК:', max = 5) 

bar.next()

res = VKontakte() # Пускаем запрос 🚀
alb_cheker = VKontakte()

if from_album == ('p' or 'P'):
    from_what = 'profile'
    res = res.downlphoto(serv_key, own_id, from_what)
elif from_album == ('w' or 'W'):
    from_what = 'wall'
    res = res.downlphoto(serv_key, own_id, from_what)
elif from_album == ('a' or 'A'):
    res = res.getalbums(serv_key, own_id)
    print(f"\n\nВыберите альбом: ")
    for i in res.json()['response']['items']:
        print(f"\nНомер альбома: {i['id']}\nНазвание альбома: {i['title']}")
    album_id = input("\nВведите номер нужного альбома: |")
    from_what = album_id
    res = alb_cheker.downlphoto(serv_key, own_id, from_what)

if 'error' in res.json():
    print('\n\nОшибка!\n')
    if res.json()['error']['error_code'] == 100:
        print('Запрашиваемый id пользователя не найден!')
        sys.exit()
    elif res.json()['error']['error_code'] == 300:
        print('Альбом переполнен! Перед продолжением работы нужно удалить лишние объекты из альбома или использовать другой альбом.')
    elif res.json()['error']['error_code'] == 30:
        print('Профиль является приватным!')
    elif res.json()['error']['error_code'] == 29:
        print('Программа перегружена :(\nПопробуйте ещё раз через некоторое время.')
    elif res.json()['error']['error_code'] == 18:
        print('Страница пользователя была удалена или заблокирована.')
    elif res.json()['error']['error_code'] == 10:
        print('Произошла внутренняя ошибка сервера. Попробуйте позже!')
    elif res.json()['error']['error_code'] == 6:
        print('Слишком много запросой в секунду. Попробуйте позже!')

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

# Полетели на диск 💽

bar = IncrementalBar('Загрузка на диск:', max = 2 + len(new_json)*2)
ya = YandexDisk(disk_token)
ya.create_folder(fold_name) # создаём папку для выгрузки 📂

bar.next()

for image in new_json: # Скачаем фотографии
    img_data = requests.get(new_json.get(image)).content
    with open(f'saved_pictures/piks_out/{image}.jpg', 'wb') as handler:
        handler.write(img_data)
    bar.next()

bar.next()

for image in new_json: # Отправим на диск 👾
    try:
        ya.upload_photo(f'{fold_name}/{image}', f'saved_pictures/piks_out/{image}.jpg')
        bar.next()
    except requests.exceptions.HTTPError:
        print('\nФото не найдено! Возможно оно не существует. Проверьте ссылку', new_json.get(image))
        bar.next()
        continue

bar.next()
bar.finish()

print('\nЗагрузка выполнена успешно!')