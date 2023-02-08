import requests
import configparser as cf # Для парса конфига
import time, vk, os
from progress.bar import IncrementalBar

config = cf.ConfigParser()
config.read("config2.ini")
disk_token = config.get('TOKEN','disk_token')
vk_token = config.get('TOKEN', 'vk_access_token')
vk_id = str(config.get('TOKEN', 'vk_user_id'))
serv_key = 'c3d398bec3d398bec3d398be24c0c11502cc3d3c3d398bea0306811fe8afcb75ebc4ae9' # Сервисный ключ доступа

URL = 'https://api.vk.com/method/photos.get'
params = {
    'access_token': serv_key,
    'owner_id':'1',
    'album_id':'profile',
    'v':'5.131'
}