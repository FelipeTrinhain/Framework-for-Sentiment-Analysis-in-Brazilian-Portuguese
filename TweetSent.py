import glob
import errno


#file_path = "D:\\Users\\Felipe\\Documents\\Projects\\Python Projects\\tweetSentBR_extracted\\tweets"

class TweetSent:

    def __init__(self, read_path):
        self.read_path = read_path

        self.file_annotated_out = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tweetSentBR_extracted/tweets/tweets_annotated_out.txt"
        self.file_out = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tweetSentBR_extracted/tweets/tweets_out.txt"

    def extract_files(self):
        pass

    def norm_tweets(self):
        f1 = open(self.file_annotated_out, "w", encoding= "utf8")
        f2 = open(self.file_out, "w", encoding= "utf8")

        file_neg = self.read_path + "/tweets.neg"
        file_neu = self.read_path + "/tweets.neu"
        file_pos = self.read_path + "/tweets.pos"

        with open(file_neg, encoding="utf8") as f:
            for line in f:
                line = line[19:len(line)-1]
                f1.write(line + "\t-1\n\n\n")
                f2.write(line + "\nMARKERENDOFREVIEW\n\n\n")

        with open(file_neu, encoding="utf8") as f:
            for line in f:
                line = line[19:len(line)-1]
                f1.write(line + "\t0\n\n\n")
                f2.write(line + "\nMARKERENDOFREVIEW\n\n\n")

        with open(file_pos, encoding="utf8") as f:
            for line in f:
                line = line[19:len(line)-1]
                f1.write(line + "\t1\n\n\n")
                f2.write(line + "\nMARKERENDOFREVIEW\n\n\n")

        f1.close()
        f2.close()
        print("Concluído TweetSent\n\n")

