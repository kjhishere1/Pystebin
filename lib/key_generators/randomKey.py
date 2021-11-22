import math
import random

class RandomKeyGenerator:
    def __init__(self, keyspace = ''):
        self.keyspace = keyspace if keyspace != '' else 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    def createKey(self, keyLength):
        text = ''
        for _ in range(keyLength):
            index = math.floor(random.random() * len(self.keyspace))
            text += self.keyspace[index]
        return text