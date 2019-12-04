import time
import copy
from Normalize import Normalize
from TwitterFilters import TwitterFilters
from SentenceSegment import SentenceSegment
from Tokenizer import Tokenizer
from OpPhrasesDetector import OpPhrasesDetector
from LexLiu import LexLiu
from Chi2 import Chi2
from SVM import SVM
from sklearn import metrics
#from sklearn.metrics import confusion_matrix, classification_report

path_buscape_reviews = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/out.txt"
path_buscape_annot = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/annotated_out.txt"
path_buscape_nointerrogation = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/out_nointerrogation.txt"
path_tweets_reviews = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tweetSentBR_extracted/tweets/tweets_out.txt"
path_tweets_annot = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tweetSentBR_extracted/tweets/tweets_annotated_out.txt"
path_temp_review = '/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tempReview.txt'
path_test_buscape = '/mnt/d/Users/Felipe/Documents/Projects/Python Projects/testReviews.txt'
path_tes_tweets = '/mnt/d/Users/Felipe/Documents/Projects/Python Projects/testReviewsTweets.txt'

path_read_buscape = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/*/*/*.xml"
path_read_tweets = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tweetSentBR_extracted/tweets"

class Liu():
    
    def __init__(self):
        self.normalize = Normalize()
        self.twitter_filters = TwitterFilters()
        #self.test_list_buscape = self.read_review(path_buscape_reviews)
        self.test_list_tweets = self.read_review(path_tweets_reviews)
        #self.annot_list_buscape = self.read_review(path_buscape_annot)
        self.annot_list_tweets = self.read_review(path_tweets_annot)
        
        self.tokenizer = Tokenizer()
        #self.sentence_segment = SentenceSegment()
        #self.opphrase = OpPhrasesDetector()
        self.lex = LexLiu()
        self.chi2 = Chi2()
        self.svm = SVM()

    def read_review(self, path):
        try:
            f = open(path, "r", encoding="utf8")
            review_list = f.read().split("\n\n\n")
            f.close()
            empty_counter = 0
            for review in review_list:
                if(review == ""):
                    empty_counter += 1
            
            for i in range(0, empty_counter):
                review_list.remove("")

            #print(empty_counter)

        except IOError as exc:
            print("Erro no arquivo")
            if exc.errno != errno.EISDIR:
                raise

        return review_list

    def raw_review(self, path):
        try:
            f = open(path, "r", encoding="utf8")
            review_list = f.read()
            #print(review)
            f.close()

        except IOError as exc:
            print("Erro no arquivo")
            if exc.errno != errno.EISDIR:
                raise

        return review_list

    def tokenize_review_list(self, review_list):

        tokenized_review_list = []

        for review in review_list:
            tokenized_review_list.append(self.tokenizer.tokenize(review))
       
        return tokenized_review_list

    def annot_review_list_liwc(self, review_list):
        pol_list = []
        t_reviews_list = self.tokenize_review_list(review_list)
        nolex_words_reviews_list = []
        counter = 0
        avg = 0
        soma = 0
        for review in t_reviews_list:
            start = time.time()
            pol, nolex_words = self.lex.annot_words_liwc(review)
            pol_list.append(pol)
            nolex_words_reviews_list.append(nolex_words)
            end = time.time()
            counter += 1
            soma = soma + (end-start)
            avg = '%.3f'%(soma/counter)
            print("LIWC\t", counter, " Time: ", '%.3f'%(end-start), " Average Time: ", avg)
        
        return pol_list, nolex_words_reviews_list

    def annot_review_list_oplexicon(self, review_list):
        pol_list = []
        t_reviews_list = self.tokenize_review_list(review_list)
        nolex_words_reviews_list = []
        counter = 0
        avg = 0
        soma = 0
        for review in t_reviews_list:
           start = time.time()
           pol, nolex_words = self.lex.annot_words_oplexicon(review)
           pol_list.append(pol)
           nolex_words_reviews_list.append(nolex_words)
           end = time.time()
           counter += 1
           soma = soma + (end-start)
           avg = '%.3f'%(soma/counter)
           print("Oplexicon\t", counter, " Time: ", '%.3f'%(end-start), " Average Time: ", avg)

        return pol_list, nolex_words_reviews_list

    def annot_review_list_sentilex(self, review_list):
        pol_list = []
        t_reviews_list = self.tokenize_review_list(review_list)
        nolex_words_reviews_list = []
        counter = 0
        avg = 0
        soma = 0
        for review in t_reviews_list:
           start = time.time()
           pol, nolex_words = self.lex.annot_words_sentilex(review)
           pol_list.append(pol)
           nolex_words_reviews_list.append(nolex_words)
           end = time.time()
           counter += 1
           soma = soma + (end-start)
           avg = '%.3f'%(soma/counter)
           print("Sentilex\t", counter, " Time: ", '%.3f'%(end-start), " Average Time: ", avg)

        return pol_list, nolex_words_reviews_list

    def sum_polarities(self, pol_list):
        pol_total = 0
        for pol in pol_list:
            pol_total = pol_total + pol
        
        return pol_total

    def make_final_pol_list(self, pol_list):
        final_pol_list = []
        
        for item in pol_list:
            final_pol_list.append(self.sum_polarities(item))
            #print(final_pol_list)

        return final_pol_list

    def normalize_pol_list(self, final_pol_list):
        
        normalized_pol_list =[]

        for pol in final_pol_list:
            if(pol > 0):
                normalized_pol_list.append(1)
            elif(pol < 0):
                normalized_pol_list.append(-1)
            else:
                normalized_pol_list.append(0)

        return normalized_pol_list

    def complete_normalize(self, pol_list):

        final_pol_list = self.make_final_pol_list(pol_list)
        normalized_pol_list = self.normalize_pol_list(final_pol_list)

        return normalized_pol_list

    def get_bunch_annot(self, annot, size):
        bunch_annot = []

        for x in range(0, size):

            bunch_annot.append(annot[x])

        return bunch_annot

    def get_pol_from_txt(self, review_list):
        pol_list = []

        for line in review_list:
            review_line_list = line.split("\t")
            
            if (len(review_line_list) > 0):
                if("0" == review_line_list[-1]):
                    pol_list.append(0)
                elif("1" == review_line_list[-1]):
                    pol_list.append(1)
                elif("-1"  == review_line_list[-1]):
                    pol_list.append(-1)
         
        return pol_list

    """def get_lex_accuracy(self, lex_annot, annot):
        if(len(lex_annot) == len(annot)):
            accur = metrics.accuracy_score(lex_annot, annot)

            return accur
        
        else:
            print("Error, different sizes for annotation lists")
            
            return"""

    def calculate_metrics(self, pol_list, annot_list): 
        normalized_pol_list = self.complete_normalize(pol_list)
        bunch_annot = self.get_bunch_annot(self.get_pol_from_txt(annot_list), len(normalized_pol_list))
        print(metrics.classification_report(normalized_pol_list, bunch_annot))
        
    def calculate_metrics_liwc(self, test_list, annot_list):
        start = time.time()
        pol_list, nolex_words_review_list = self.annot_review_list_liwc(test_list)
        end = time.time()
        print("ANNNOT\t Time: ", '%.3f'%(end-start))
       
        self.calculate_metrics(pol_list, annot_list)
        

    def calculate_metrics_oplexicon(self, test_list, annot_list):

        pol_list = self.annot_review_list_oplexicon(test_list)
        self.calculate_metrics(pol_list, annot_list)

    def calculate_metrics_sentilex(self):
        
        pol_list = self.annot_review_list_sentilex(test_list)
        self.calculate_metrics(pol_list, annot_list)

    def remove_lexwords_reviews(self, review_list, lexicon):
        nolexwords_review_list = self.tokenize_review_list(review_list)
        s1 = []
        #print(nolexwords_review_list)
        for word in lexicon:
            #print(word[0])
            for review in nolexwords_review_list:
                for token in review:
                    if(word[0] == token.lower()):
                        review.remove(token)
            #print(word[0])
        for review in nolexwords_review_list:
                s1.append(" ".join(review))

        
        return s1

    def extract_neutral_reviews(self, pol_list, review_list):
        extracted_neu_reviews_list = []
        indexes_to_remove = []
        new_pol_list = copy.deepcopy(pol_list)
        new_review_list = copy.deepcopy(review_list)
        #new_annot_list = copy.deepcopy(annot_list)

        for i in range(0, len(pol_list)):
            if(pol_list[i] == 0):
                extracted_neu_reviews_list.append(review_list[i])
                indexes_to_remove.append(i)

        for index in indexes_to_remove:
            review_list[index] = "0"
            new_review_list[index] = "0"

        for pol in pol_list:
            if(pol == 0):
                new_pol_list.remove(pol)

        for review in review_list:
            if(review == "0"):
                new_review_list.remove(review)

        
        return extracted_neu_reviews_list, new_review_list, new_pol_list, indexes_to_remove

    def format_reviews_svm(self, reviews_dtm, indexes):
        test_reviews = []
        train_reviews = []
       # for index in indexes:
        #    extracted_dtm.append(reviews_dtm[index])

        for i in range(0, len(reviews_dtm)):
            for index in indexes:
                if(i == index):
                    test_reviews.append(reviews_dtm[index])
                    break
            else:
                train_reviews.append(reviews_dtm[index])


        return test_reviews, train_reviews

    def exec_chi2(self, pol_reviews, pol_list):
        df = self.chi2.x_to_dataframe(pol_reviews)
        chi2_score = self.chi2.calculate_chi2(df, pol_list)
        pos_to_extract = self.chi2.get_position_to_extract(chi2_score)
        opinion_indicators = self.chi2.get_features(df, pos_to_extract)

        return opinion_indicators

    def opinion_is_inreview(self, review, indicators):
        for ind in indicators:
            for word in review:
                if(ind == word):
                    return True

        return False

    def find_opinion_reviews(self, indicators, reviews):
        t_reviews = self.tokenize_review_list(reviews)
        indexes_exct_neu_reviews = []

        opinion_reviews = []

        for review in t_reviews:
            if(self.opinion_is_inreview(review, indicators)):
                opinion_reviews.append(" ".join(review))
                indexes_exct_neu_reviews.append(t_reviews.index(review))

        return opinion_reviews, indexes_exct_neu_reviews

    def translate_indexes(self, neu_indexes, exct_neu_indexes):
        new_indexes = []

        for index in exct_neu_indexes:
            new_indexes.append(neu_indexes[index])

        return new_indexes

    def select_test_reviews(self, test_reviews, exct_indexes):
        new_test_reviews = []

        for index in exct_indexes:
            new_test_reviews.append(test_reviews[index])

        return new_test_reviews

    def make_analysis_list(self, pol_list, to_append_pol):
        
        for item in to_append_pol:
            pol_list.append(item)

    def make_annot_pol_list(self, annot_reviews, size, indexes_to_remove, indexes_to_append):
        annot_pol_list = []

        pol_list = self.get_bunch_annot(self.get_pol_from_txt(annot_reviews), size)

        for i in range(0, len(pol_list)):
            if(i not in (indexes_to_remove)):
                annot_pol_list.append(pol_list[i])

        for index in indexes_to_append:
            annot_pol_list.append(pol_list[index])

        return annot_pol_list


start_total = time.time()            
liu = Liu()
#t_reviews_list = liu.tokenizer.tokenize(liu.test_list_tweets[1755])
#pol, nolex_words = liu.lex.annot_words_liwc(t_reviews_list)

#liu.twitter_filters.all_filters()
#print(liu.test_list_buscape)
#liu.normalize.tweetsent(path_read_tweets)
#annot = liu.normalize.buscape(path_read_buscape)

pol_list, nolex_words_review_list = liu.annot_review_list_sentilex(liu.test_list_tweets)
#print(len(nolex_words_review_list))
normalized_pol_list = liu.complete_normalize(pol_list)
print("Extracting neutral Reviews\n")
neu_reviews, pol_reviews, train_pol, neu_indexes = liu.extract_neutral_reviews(normalized_pol_list, nolex_words_review_list)
print("Finished extracting neutral reviews\n")


print("Executing Chi2\n")
opinion_indicators = liu.exec_chi2(pol_reviews, train_pol)
print("Finished Chi2\n")

print("Searching for extra opinative reviews\n")
extra_opinion_reviews, ind_exct_neu_reviews = liu.find_opinion_reviews(opinion_indicators, neu_reviews)
print("Finished search\n")

print("Creating DataFrame\n")
reviews_dtm = liu.svm.x_to_dataframe(nolex_words_review_list)
test_reviews, train_reviews = liu.format_reviews_svm(reviews_dtm, neu_indexes)
print("Finished Dataframe\n")

print("Selecting reviews for test\n")
test_reviews = liu.select_test_reviews(test_reviews, ind_exct_neu_reviews)

print("Training model\n")
train_model = liu.svm.train_svm_model(train_reviews, train_pol)
predict_list = liu.svm.test_svm_model(test_reviews, train_model)
print("Finished Training\n")

print("Making Analysis\n")
liu.make_analysis_list(train_pol, predict_list)
indexes_to_append = liu.translate_indexes(neu_indexes, ind_exct_neu_reviews)
annot_list = liu.make_annot_pol_list(liu.annot_list_tweets, len(normalized_pol_list), neu_indexes, indexes_to_append)
print("Predict:\t", len(train_pol), "\nAnnot:\t", len(annot_list))
print()
print(metrics.classification_report(train_pol, annot_list))

end_total = time.time()
print("TOTAL TIME\t: ", '%.3f'%(end_total-start_total))