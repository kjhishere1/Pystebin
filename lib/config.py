import json


class Config(object):
    def __init__(self, json: dict):
        self.dict = json
        for key in json:
            Type = type(json[key])
            if Type == dict:
                setattr(self, key, Config(json[key]))
            else:
                setattr(self, key, json[key])


    def __iter__(self):
        for x, y in self.dict.items():
            yield x, y


    def __getattr__(self, name):
        setattr(self, name, None)
        return None
