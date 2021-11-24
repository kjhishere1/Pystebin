import os
import hashlib


class FileDocumentStore:
    def __init__(self, options):
        self.basePath = options.path or './data'
        self.expire = options.expire


    def md5(self, str):
        md5sum = hashlib.md5()
        md5sum.update(str)
        return md5sum.hexdigest()


    def set(self, key, data, skipExpire=None):
        try:
            os.makedirs(self.basePath, exist_ok=True)
            fn = self.basePath + '/' + self.md5(key)
            with open(fn, 'w', encoding='UTF-8') as file:
                file.write(data)
            return True
        except Exception as err:
            print(err)


    def get(self, key, skipExpire=None):
        fn = self.basePath + '/' + self.md5(key)
        try:
            with open(fn, 'r', encoding='UTF-8') as file:
                data = file.read()
            return data
        except Exception:
            return False


Store = FileDocumentStore