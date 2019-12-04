import errno
import copy
import re

class LexLiu:
    def __init__(self):
        
        self.oplexicon_path = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/OpLexicon/lexico_v3.0.txt"
        self.liwc_path = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/LIWC/LIWC2007_Portugues_win.dic.txt"
        self.sentilex_path = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/SentiLex-PT02/SentiLex-flex-PT02.txt"

        self.additives_conj_list = ["e"]
        self.adversative_conj_list = ["não", "nao"]##, "porém", "contudo", "todavia", "entretanto", "senão", "entanto", "obstante", "apesar"] comentar na escrita que para nivel de documento nao funciona tao bem
        self.intesifiers_list = []

        self.liwc = self.read_liwc()
        self.oplexicon = self.read_oplexicon()
        self.sentilex = self.read_sentilex()

    def read_liwc(self):

        formatted_liwc = []

        try:
            f = open(self.liwc_path, "r", encoding="utf8")
            liwc = f.readlines()
            f.close()
            for line in liwc:
                a_list = line.split()
                if("126" in a_list):
                    formatted_liwc.append([a_list[0], 1])
                elif("127" in a_list):
                    formatted_liwc.append([a_list[0], -1])
            
        except IOError as exc:
            print("Erro no arquivo")
            if exc.errno != errno.EISDIR:
                raise

        return formatted_liwc

    def read_oplexicon(self):
        formatted_oplexicon = []

        try:
            f = open(self.oplexicon_path, "r", encoding="utf8")
            oplexicon = f.readlines()
            f.close()

            for line in oplexicon:
                a_list = line.split(",")
                if("1" in a_list):
                    formatted_oplexicon.append([a_list[0], 1])
                elif("-1" in a_list):
                    formatted_oplexicon.append([a_list[0], -1])
            
        except IOError as exc:
            print("Erro no arquivo")
            if exc.errno != errno.EISDIR:
                raise

        return formatted_oplexicon

    def read_sentilex(self):
        formatted_sentilex = []

        try:
            f = open(self.sentilex_path, "r", encoding="utf8")
            sentilex = f.readlines()
            f.close()

            for line in sentilex:
                a_list = re.split(";|,|.PoS|=", line)
                if("POL:N1" in a_list):
                    pol = int(a_list[a_list.index("POL:N1")+1])
                    #str = str.split("=")
                    #pol = int(str[1])
                    formatted_sentilex.append([a_list[0], a_list[1], pol])
                else:
                    pol = int(a_list[a_list.index("POL:N0")+1])
                    #str = str.split("=")
                    #pol = int(str[1])
                    formatted_sentilex.append([a_list[0], a_list[1], pol])
                #elif("-1" in a_list):
                 #   formatted_oplexicon.append([a_list[0], "-1"])
            
        except IOError as exc:
            print("Erro no arquivo")
            if exc.errno != errno.EISDIR:
                raise

        return formatted_sentilex

    def search_liwc(self, word):

        polarity = 0

        for line in self.liwc:    
            if(word.lower() == line[0]):
                 polarity = line[1]
                 #print(line)
                        
                 return polarity

        return polarity

    def search_sentilex(self, word):
        
        polarity = 0

        for line in self.sentilex:    
            if(word.lower() == line[0]):
                 polarity = line[2]
                        
                 return polarity

            elif(word.lower() == line[1]):
                 polarity = line[2]
                        
                 return polarity

        return polarity

    def search_oplexicon(self, word):
        polarity = 0

        for line in self.oplexicon:    
            if(word.lower() == line[0]):
                 polarity = line[1]
                 #print(line)
                        
                 return polarity

        return polarity

    def annot_words_liwc(self, tokenized_review):
        nolexwords_t_review = copy.deepcopy(tokenized_review)
        annot_words_list = []
        conj = 0
        modifier = 1
        #polarity = 0
        
        #for word in tokenized_review:
        for i in range(0, len(tokenized_review)):  
            if(tokenized_review[i].lower() in self.adversative_conj_list):
                modifier = -1
                
                if(i < len(tokenized_review)-1):
                    continue

            elif(tokenized_review[i].lower() in self.intesifiers_list):
                elem = self.intesifiers_list[self.intesifiers_list.index(tokenized_review[i].lower())]
                modifier = elem[1]
                continue

            elif(tokenized_review[i].lower() in self.additives_conj_list):
                conj = 1
                
            else:
                annot = self.search_liwc(tokenized_review[i])
                if(annot != 0):
                    if(conj == 1):
                        if(len(annot_words_list)>0):
                            annot = annot_words_list[-1]
                            conj = 0                        
                    annot_words_list.append(modifier*annot)
                    nolexwords_t_review.remove(tokenized_review[i])
                    modifier = 1

            if(len(nolexwords_t_review) > 0):
                nolexwords_review = " ".join(nolexwords_t_review)
            else:
                nolexwords_review = " ".join(tokenized_review)
                
        return annot_words_list, nolexwords_review

    def annot_words_oplexicon(self, tokenized_review):
        nolexwords_t_review = copy.deepcopy(tokenized_review)
        annot_words_list = []
        conj = 0
        modifier = 1
        #polarity = 0
       
        #for word in tokenized_review:
        for i in range(0, len(tokenized_review)):
            if(tokenized_review[i].lower() in self.adversative_conj_list):
                modifier = -1
                
                if(i < len(tokenized_review)-1):
                    continue

            elif(tokenized_review[i].lower() in self.intesifiers_list):
                elem = self.intesifiers_list[self.intesifiers_list.index(tokenized_review[i].lower())]
                modifier = elem[1]
                continue

            elif(tokenized_review[i].lower() in self.additives_conj_list):
                conj = 1
                
            else:
                annot = self.search_oplexicon(tokenized_review[i])
                if(annot != 0):
                    if(conj == 1):
                        if(len(annot_words_list)>0):
                            annot = annot_words_list[-1]
                            conj = 0                        
                    annot_words_list.append(modifier*annot)
                    nolexwords_t_review.remove(tokenized_review[i])
                    modifier = 1

            if(len(nolexwords_t_review) > 0):
                nolexwords_review = " ".join(nolexwords_t_review)
            else:
                nolexwords_review = " ".join(tokenized_review)
        
        return annot_words_list, nolexwords_review

    def annot_words_sentilex(self, tokenized_review):
        nolexwords_t_review = copy.deepcopy(tokenized_review)
        annot_words_list = []
        conj = 0
        modifier = 1
        #polarity = 0
       
        #for word in tokenized_review:
        for i in range(0, len(tokenized_review)):
            if(tokenized_review[i].lower() in self.adversative_conj_list):
                modifier = -1
                
                if(i < len(tokenized_review)-1):
                    continue

            elif(tokenized_review[i].lower() in self.intesifiers_list):
                elem = self.intesifiers_list[self.intesifiers_list.index(tokenized_review[i].lower())]
                modifier = elem[1]
                continue

            elif(tokenized_review[i].lower() in self.additives_conj_list):
                conj = 1
                
            else:
                annot = self.search_sentilex(tokenized_review[i])
                if(annot != 0):
                    if(conj == 1):
                        if(len(annot_words_list)>0):
                            annot = annot_words_list[-1]
                            conj = 0                        
                    annot_words_list.append(modifier*annot)
                    nolexwords_t_review.remove(tokenized_review[i])
                    modifier = 1

            if(len(nolexwords_t_review) > 0):
                nolexwords_review = " ".join(nolexwords_t_review)
            else:
                nolexwords_review = " ".join(tokenized_review)
        
        return annot_words_list, nolexwords_review
