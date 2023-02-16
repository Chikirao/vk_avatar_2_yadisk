import requests

class VKontakte:

    def downlphoto(self, ukey, uid, fromwh):
        URL = 'https://api.vk.com/method/photos.get'
        params = {
        'access_token': ukey,
        'owner_id': uid,
        'album_id': fromwh,
        'v':'5.131',
        'extended':'1'
        }
        return requests.get(URL, params=params)
    
    def getalbums(self, ukey, uid):
        URL = 'https://api.vk.com/method/photos.getAlbums'
        params = {
        'access_token': ukey,
        'owner_id': uid,
        'v':'5.131',
        'extended':'1'
        }
        return requests.get(URL, params=params)