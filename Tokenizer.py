from nltk.tokenize import word_tokenize
import errno

file_path = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tweetSentBR_extracted/tweets_out.txt"

class Tokenizer:
    def __init__(self):
        pass

    def tokenize(self, text):

            list = word_tokenize(text)
        
            return list
