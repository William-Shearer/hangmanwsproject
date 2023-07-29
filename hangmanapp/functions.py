from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from random import randint

"""
# A test fiunction. Vestigial now. Reference.
def load_words():
    try:
        wordfile = default_storage.open("wordbank/nouns_en.txt")
        words = wordfile.read().decode().split()
        return words
    except FileNotFoundError:
        return False
"""

def get_word():
    try:
        # Load a file of the wordbank for the game.
        # Note, use Django's own system. It does not like using Python's file loader directly.
        wordfile = default_storage.open("wordbank/nouns_en.txt")
        # This breaks the file content up into a list of strings.
        words = wordfile.read().decode().split()
        # Randomly select a word from the file.
        word = words[randint(0, len(words) - 1)]
        # Return the word as a list of the letters.
        return [c for c in word]
    except FileNotFoundError:
        return False