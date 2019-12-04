import errno
import time
from Normalize import Normalize
from TwitterFilters import TwitterFilters
from POSTagger import POSTagger
from PMI import PMI
from sklearn import metrics

class Turney():
    
    def __init__(self):
        self.buscape_dataset_path = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/*/*/*.xml"
        self.twitter_dataset_path = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tweetSentBR_extracted/tweets"
        self.tagger_temp_path = '/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tempReview.txt'
        self.treetagger_out = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/saidaTTag.txt"
        self.freeling_out = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/saidaFreeling.txt"
        self.linguakit_out = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/saidaLinguakit.txt"
        self.buscape_annot_out = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/annotated_out.txt"
        self.buscape_out = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/out.txt"
        #self.buscape_annotations = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/annotations.txt"

        #self.tagset = ["A", "C", "D", "N", "P", "R", "S", "V", "Z", "W", "I", "F"]
        self.adjective = "A"
        self.noun = "N"
        self.adverb = "R"
        self.verb = "V"

        self.normalize = Normalize()
        self.twitter_filters = TwitterFilters()
        self.tagger = POSTagger()
        self.PMI = PMI(self.buscape_out)

        self.review_list = self.PMI.review_list
        self.buscape_annot_list = self.get_buscape_annotations()
    
    def exec_norm_buscape(self):
        self.normalize.buscape(self.buscape_dataset_path)

    def exec_norm_twitter(self):
        self.normalize.tweetsent(self.twitter_dataset_path)

    def exec_twitter_filters(self):
        self.twitter_filters.all_filters()

    def list_tagged_words(self, path):
        words_list = []

        try:
            f = open(path, "r", encoding="utf8")
            lines = f.readlines()
            f.close()

        except IOError as exc:
            print("Erro no arquivo")
            if exc.errno != errno.EISDIR:
                raise

        for line in lines:
            words_list.append(line.split())
        #print(words_list)
        return words_list

    def find_pattern_FL(self, tagged_words):
        extracted_words_list = []
          
        for x in range(len(tagged_words)-1):
            #print(x)
            #print(tagged_words[x])
            if(tagged_words[x]==[]):
                continue
            if(tagged_words[x][2][0] == self.adjective):  #Tests if word is JJ
                if(x < (len(tagged_words)-1)):
                    if(tagged_words[x+1][2][0] == self.noun ):  #Tests if next word is NN
                        extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0]) #Extract Turney's first pattern JJ NN

                    elif(tagged_words[x+1][2][0] == self.adjective):
                        if(x < (len(tagged_words)-2)):
                            if(tagged_words[x+2][2][0] != self.noun ):
                                extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0]) #extract Turney's third pattern JJ JJ
                        elif(x == (len(tagged_words)-2)):
                            extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0])

            elif(tagged_words[x][2][0] == self.adverb):   #Tests if word is RB
                if(x < (len(tagged_words)-1)):
                    if(tagged_words[x+1][2][0] == self.verb ):  #Tests if next word is VB
                        extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0]) #Extract Turney's fifth pattern RB VB

                    elif(tagged_words[x+1][2][0] == self.adjective):
                        if(x < (len(tagged_words)-2)):
                            if(tagged_words[x+2][2][0] != self.noun ):
                                extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0]) #extract Turney's second pattern RB JJ
                        elif(x == (len(tagged_words)-2)):
                            extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0])

            elif(tagged_words[x][2][0] == self.noun):    #Tests if word is NN
                if(x < (len(tagged_words)-1)):
                    if(tagged_words[x+1][2][0] == self.adjective):   #Tests if next word is JJ
                            if(x < (len(tagged_words)-2)):
                                if(tagged_words[x+2][2][0] != self.noun ):
                                    extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0]) #extract Turney's third pattern NN JJ
                            elif(x == (len(tagged_words)-2)):
                                extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0])
        print(extracted_words_list)
        return extracted_words_list

    def find_pattern_TreeTagger(self, tagged_words):
        extracted_words_list = []
        
        for x in range(len(tagged_words)-1):
            if(tagged_words[x][1][0] == self.adjective):  #Tests if word is JJ
                if(x < (len(tagged_words)-1)):
                    if(tagged_words[x+1][1][0] == self.noun ):  #Tests if next word is NN
                        extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0]) #Extract Turney's first pattern JJ NN

                    elif(tagged_words[x+1][1][0] == self.adjective):
                        if(x < (len(tagged_words)-2)):
                            if(tagged_words[x+2][1][0] != self.noun ):
                                extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0]) #extract Turney's third pattern JJ JJ
                        elif(x == (len(tagged_words)-2)):
                            extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0])

            elif(tagged_words[x][1][0] == self.adverb):   #Tests if word is RB
                if(x < (len(tagged_words)-1)):
                    if(tagged_words[x+1][1][0] == self.verb ):  #Tests if next word is VB
                        extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0]) #Extract Turney's fifth pattern RB VB

                    elif(tagged_words[x+1][1][0] == self.adjective):
                        if(x < (len(tagged_words)-2)):
                            if(tagged_words[x+2][1][0] != self.noun ):
                                extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0]) #extract Turney's second pattern RB JJ
                        elif(x == (len(tagged_words)-2)):
                            extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0])

            elif(tagged_words[x][1][0] == self.noun):    #Tests if word is NN
                if(x < (len(tagged_words)-1)):
                    if(tagged_words[x+1][1][0] == self.adjective):   #Tests if nexto word is JJ
                            if(x < (len(tagged_words)-2)):
                                if(tagged_words[x+2][1][0] != self.noun ):
                                    extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0]) #extract Turney's third pattern NN JJ
                            elif(x == (len(tagged_words)-2)):
                                extracted_words_list.append(tagged_words[x][0] + " " + tagged_words[x+1][0])

        return extracted_words_list

    def calculate_review_so(self, extracted_words_list):
        review_so = 0
        for item in extracted_words_list:
            review_so += self.PMI.so(item)
            #print(review_so)
        if((len(extracted_words_list)) > 0):
            review_so = review_so/len(extracted_words_list)
       
        return review_so

    def gen_so_list(self, review_list):
        so_list =[]
        soma = 0
        x=0
        #for x in range(len(review_list)-1):
        start = time.time() 
        self.tagger.freeling(review_list[1])
        tagged_words = self.list_tagged_words(self.freeling_out)
        #print(tagged_words)
        extracted_list = self.find_pattern_FL(tagged_words)
        so_list.append(self.calculate_review_so(extracted_list))
        end = time.time()
        soma = soma + (end-start)
        avg = '%.3f'%(soma/(x+1))
        print("TreeTagger\t", x, " Time: ", '%.3f'%(end-start), " Average Time: ", avg, "SO List: ", so_list[x])

        return so_list
    
    def get_buscape_annotations(self):
        pol_list = []
        try:
            f = open(self.buscape_annot_out, "r", encoding="utf8")
            review_list = f.read().split("\n\n\n")
            f.close()

            for line in review_list:
                review_line_list = line.split("\t")
            
                if (len(review_line_list) > 0):
                    if("0" == review_line_list[-1]):
                        pol_list.append(0)
                    elif("1" == review_line_list[-1]):
                        pol_list.append(1)
                    elif("-1"  == review_line_list[-1]):
                        pol_list.append(-1)

        except IOError as exc:
                print("Erro no arquivo")
                if exc.errno != errno.EISDIR:
                    raise

        return pol_list

    def normalize_pol_list(self, pol_list):
        
        normalized_pol_list =[]

        for pol in pol_list:
            if(pol > 0):
                normalized_pol_list.append(1)
            elif(pol < 0):
                normalized_pol_list.append(-1)
            else:
                normalized_pol_list.append(0)

        return normalized_pol_list
    


start_total = time.time()        
turney = Turney()

turney.exec_norm_twitter()
turney.exec_twitter_filters()
#so_list = turney.gen_so_list(turney.review_list)
#normalized_so_list = turney.normalize_pol_list(so_list)
#print(so_list)
#print(normalized_so_list)
#print(metrics.classification_report(so_list, buscape_annot_list))

end_total = time.time()
print("TOTAL TIME\t: ", '%.3f'%(end_total-start_total))


