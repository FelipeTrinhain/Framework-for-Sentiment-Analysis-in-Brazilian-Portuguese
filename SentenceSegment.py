from nltk import sent_tokenize
import errno


class SentenceSegment:
    def __init__(self):
       pass

    def tokenize(self, text):

        list = sent_tokenize(text)
        return list

