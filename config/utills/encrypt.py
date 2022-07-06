from django.conf import settings
import hashlib


def md5(data_sting):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_sting.encode('utf-8'))
    return obj.hexdigest()