import json


class Config(object):
    def __init__(self, json: dict):
        self._json = json
        for key in json:
            Type = type(json[key])
            if Type == str:
                exec(f"self.{key} = '{json[key]}'")
            elif Type == dict:
                exec(f"self.{key} = Config({json[key]})")
            else:
                exec(f"self.{key} = {json[key]}")


    def __iter__(self):
        for x, y in self._json.items():
            yield x, y


    def __getattribute__(self, name):
        try:
            return super(Config, self).__getattribute__(name)
        except AttributeError as ae:
            return None