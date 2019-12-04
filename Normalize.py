from Buscape import Buscape
from TweetSent import TweetSent

#path_read = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/*/*/*.xml"
#file_path = "D:\\Users\\Felipe\\Documents\\Projects\\Python Projects\\tweetSentBR_extracted\\tweets"
#file_path = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tweetSentBR_extracted/tweets"
class Normalize:

    def __init__(self):
        pass
        #self.dataset_path = dataset_path

    def buscape(self, dataset_path):
        buscape = Buscape(dataset_path)
        annot = buscape.norm_buscape()
        
        return annot

    def tweetsent(self, dataset_path):
        tweet = TweetSent(dataset_path)
        tweet.norm_tweets()


#Normalize(path_read).buscape()
#Normalize(file_path).tweetsent()