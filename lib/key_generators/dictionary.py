import re
import math
import random

class DictionaryGenerator:
    def __init__(options):
        ## Check options format
        if not options:       raise Exception('No options passed to generator')
        if not options['path']:  raise Exception('No dictionary path specified in options')

        ## Load dictionary
        with open(options['path'], 'r', encoding='utf8') as File:
            data = File.read()
            self.dictionary = re.split(r'/[\n\r]+/', data)

    ## Generates a dictionary-based key, of keyLength words
    def createKey(self, keyLength):
        let text = ''
        for _ in range(keyLength):
            index = math.floor(random.random() * len(self.dictionary))
            text += self.dictionary[index]
        return text