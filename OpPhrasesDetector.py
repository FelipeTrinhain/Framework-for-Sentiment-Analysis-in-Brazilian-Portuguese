import errno
from SentenceSegment import SentenceSegment
from Tokenizer import Tokenizer
import copy

class OpPhrasesDetector():
    
    def __init__(self):
        #self.document = document
        self.question_words_list = ["QUAL", "QUAIS", "QUE", "QUÊ", "ONDE", "QUANDO", "QUEM"]
        self.question_bigram = ["O", "POR"]
        self.question_mark = "?"

    def extract_text(self):
        try:
            f = open(self.document, "r", encoding="utf8")
            list = f.read().split("\n\n\n")
            f.close()

        except IOError as exc:
            print("Erro no arquivo")
            if exc.errno != errno.EISDIR:
                raise

        return list

    def write_text(self, path, words_list):
        open(path, "w").close()
        f = open (path, "a", encoding="utf8")
        for review in words_list:
            for sentence in review:
                for word in sentence:
                    f.write(word)
                    f.write(" ")
            f.write("\n\n\n")

        f.close()

    def sent_segment(self, text):
        review = SentenceSegment().tokenize(text)

        return review

    def sent_append(self, a_list):
        #a_list = self.extract_text()

        for review in a_list:
            a_list[a_list.index(review)] = self.sent_segment(review)

        return a_list

    def word_segment(self, sentence):
        a_list = Tokenizer().tokenize(sentence)

        return a_list

    def words_append(self, a_list):

        new_list = copy.deepcopy(a_list)

        for review in new_list:
            for sentence in review:
                review[review.index(sentence)] = self.word_segment(sentence)

        return new_list

    def check_question_bigram(self, a_list, a_str):
            if(a_list[a_list.index(a_str)-1] in self.question_bigram):
                return True
            else:
               return False

    def sentence_isinterrogation(self, sentence):
        for word in sentence:
            if(word.upper() in self.question_words_list):
                if((word.upper() == self.question_words_list[2]) or (word.upper() == self.question_words_list[3])):
                    if(self.check_question_bigram(sentence, word)):
                        pass
                    else:
                        continue

                if(self.question_mark == sentence[len(sentence)-1]):
                    return True
                else:
                    False

    def reconstruct_words_list(self, reviews_list):
        sentence_list = self.sent_append(reviews_list)
        words_list = self.words_append(sentence_list)
        for review in words_list:
            for sentence in review:
                if(self.sentence_isinterrogation(sentence)):
                    #print(review, "\n\n")
                    review.remove(sentence)
        return words_list

    def exec_opphrases(self, reviews_list, out_file):
        words_list = self.reconstruct_words_list(reviews_list)
        self.write_text(out_file, words_list)


