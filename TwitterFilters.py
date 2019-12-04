#!/usr/bin/python
import errno
import re

#test_path = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tweetSentBR_extracted/teste2.txt"

class TwitterFilters:
    
    def __init__(self):
        self.path = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tweetSentBR_extracted/tweets/tweets_out.txt"
       # self.path_annot = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tweetSentBR_extracted/tweets_annotated_out.txt"

    def __del_rt_infile(self):
        contents = ""
        try:
            f = open(self.path, "r", encoding="utf8")
            lines = f.readlines()
            for line in lines:
                if (line[0:3] == "RT "):
                    pos = lines.index(line)
                    lines.remove(line)
                    lines.pop(pos)
                    lines.pop(pos)
                    #lines.remove("\n")
                    #lines.remove("\n")
                    #print(lines)
            f.close()
        
        except IOError as exc:
            print("Erro no arquivo")
            if exc.errno != errno.EISDIR:
                raise

        try:
            f = open(self.path, "w+", encoding="utf8")
            f.writelines(lines)
            f.close()

        except IOError as exc:
            print("Erro no arquivo")
            if exc.errno != errno.EISDIR:
                raise

    def del_rt(self):
        self.__del_rt_infile()
        #self.__del_rt_infile(self.path_annot)

    def __del_words_tweetsent_infile(self):
        try:
            f = open(self.path, "r", encoding = "utf8")
            text = f.read()
            text = re.sub(r" ?NUMBER ?", " ", text)
            text = re.sub(r" ?USERNAME ?", " ", text)
            text = re.sub(r" ?http\S+ ?", " ", text)
            text = re.sub(r" ?@\S+ ?", " ", text)
            f.close()

        except IOerror as exc:
            print("Erro ao abrir arquivo")
            if exc.errno != errno.EISDIR:
                raise
        try:
            f = open(self.path, "w", encoding = "utf8")
            
            f.write(text)
            f.close()

        except IOerror as exc:
            print("Erro ao abrir arquivo")
            if exc.errno != errno.EISDIR:
                raise

    def del_words_tweetsent(self):
        self.__del_words_tweetsent_infile()
        #self.__del_words_tweetsent_infile(self.path_annot)

    def all_filters(self):
        self.del_rt()
        self.del_words_tweetsent()
        print("Filtros do Twitter Concluídos")

    def redo_abbrev(self):
        pass


#twitter = TwitterFilters(file_path, file_path_annot)
#twitter.del_rt()
#twitter.del_words_tweetsent()
