## Draws inspiration from pwgen and http://tools.arantius.com/password
import math
import random

def randOf(collection):
    return lambda: collection[math.floor(random.random() * len(collection))]

## Helper methods to get an random vowel or consonant
randVowel = randOf('aeiou')
randConsonant = randOf('bcdfghjklmnpqrstvwxyz')

class PhoneticKeyGenerator:
  ## Generate a phonetic key of alternating consonant & vowel

  @staticmethod
  def createKey(keyLength):
      text = ''
      start = math.floor(random.random() + 0.5)

      for i in range(keyLength):
          text += randConsonant() if (i % 2 == start) else randVowel()

      return text