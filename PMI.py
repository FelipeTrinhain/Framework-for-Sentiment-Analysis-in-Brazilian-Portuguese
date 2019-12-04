#from googleapiclient.discovery import build
import pprint
import nltk
from Tokenizer import Tokenizer
from math import log2
import errno

file_path = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/out.txt"

class PMI:
    
    def __init__(self, document):
        self.document = document
        self.api_key = ""
        self.cse_id = ""
        #self.text = Tokenizer(self.document).tokenize()
        self.text = self.read_document()
        self.review_list = self.split_document()

    def read_document(self):
        try:
            f = open(self.document, "r", encoding="utf8")
            text = f.read()#.replace('\n', " ")
            f.close()

        except IOError as exc:
            print("Erro no arquivo")
            if exc.errno != errno.EISDIR:
                raise
        #text = text.split(" ")
        return text

    def split_document(self):
        a_list = self.text.split("\n\n\n")

        return a_list

    def pmi(self, phrase1, phrase2):
        p_phrase1 = self.pphrase(phrase1) + 0.01
        #print(phrase1,p_phrase1)
        p_phrase2 = 1#self.pphrase(phrase2) + 0.01
        #print(phrase2, p_phrase2)
        p_coocur = self.co_occur(phrase1, phrase2) + 0.01
        #print("co ocorencia: ",p_coocur)
        
        pmi_res = log2((p_coocur)/(p_phrase1*p_phrase2))
        
        return pmi_res

    def so(self, phrase):
        pmi_excelente = self.pmi(phrase, "excelente")
        #print(phrase," pmi_excelente: ",pmi_excelente, "\n")
        pmi_ruim = self.pmi(phrase, "ruim")
        #print(phrase, "pmi_ruim: ",pmi_ruim, "\n")
        so = pmi_excelente - pmi_ruim
        return so

    def pphrase(self, phrase):
        freq = self.text.upper().count(phrase.upper())
        return freq

    def co_occur(self, phrase1, phrase2):
        co_occur_freq = 0
        for review in self.review_list:
            if(phrase1.upper() in review.upper()):
                #print(review,"\n")
                if(phrase2.upper() in review.upper()):
                    #print(review,"\n\n")
                    co_occur_freq += 1
        return co_occur_freq

    def search_google(self, search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return int(res['searchInformation']['totalResults'])

    def pmi_ir(self, phrase1, phrase2):
        query = phrase1 +" "+"AROUND(10)"+" "+ phrase2
        results = self.search_google(query, self.api_key, self.cse_id, num=10)
        return results

    def so_google(self, phrase):
        excelent_pmi = self.pmi_ir(phrase, "excelente")
        poor_pmi = self.pmi_ir(phrase, "péssimo")
        excelent_hits = self.search_google('excelente', self.api_key, self.cse_id, num=10)
        poor_hits = self.search_google('péssimo', self.api_key, self.cse_id, num=10)
        #print("Around Excelente: ", excelent_pmi)
        #print("Excelente: ", excelent_hits)
        #print("Around Péssimo: ", poor_pmi)
        #print("Péssimo: ", poor_hits)
        num = excelent_pmi*poor_hits
        den = poor_pmi*excelent_hits
        number = num/den
        sem_orientation = log2(number)
        return sem_orientation

#print(PMI(file_path).pmi("excelente", "péssimo"))
#print(PMI(file_path).co_occur("o que gostei", "o que não gostei"))
#print(PMI(file_path).pphrase(""))
#print("SO: ", PMI(file_path).so("ótimo"), "\n\n")