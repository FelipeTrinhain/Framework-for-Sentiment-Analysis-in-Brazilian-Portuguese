import glob
import os
import errno
import sys

class Buscape:
    
    def __init__(self, read_path):
        self.read_path = read_path
        
        #initializes the path of the archive containing the documents with reviews.
        #method used to read files in an folder.
        self.files = glob.glob(self.read_path)


        #initialize the path of the output file which will contain a normalized file with all reviews and thumbs Up and Down values.
        self.writefile_path = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/annotated_out.txt"
        self.writefile_path2 = "/mnt/d/Users/Felipe/Documents/Projects/Python Projects/Reviews_corpus_buscape/out.txt"

        self.review_counter = 0
        self.pos_counter = 0
        self.neg_counter = 0


    #This method access file by file in a directory folder and writes an output containing
    #the users opinion, thumbsUp and thumbsDown values refering the reviews.
    def search_in_files(self, archive, writefile, writefile2):
        f_out_annot = open (writefile, "a", encoding="utf8")
        f_out = open (writefile2, "a", encoding="utf8")
        annot = []
        
        for name in archive:
            try:
                with open(name, encoding="utf8") as f_in: 
                    print(name, end = "\r")
                    if self.test_formatting(f_in): #If the file is not in the correct formatting, jumps to the next file.
                        recommends_value = self.searching_recommends_value(f_in)
                        if (recommends_value != "-1"  and recommends_value != "1"): #Tests if recommends value is 0 or 1, else ignores the file.
                            continue
                        opinion_str = self.searching_opinion(f_in)
                        if(opinion_str == ""):
                            continue  
                        self.review_counter = self.review_counter + 1
                        if(recommends_value == "-1"):
                            self.neg_counter = self.neg_counter + 1
                            annot.append(-1)
                        else:
                            self.pos_counter = self.pos_counter + 1
                            annot.append(1)
                    else:
                        continue

                #Writes in the output file the data collected from the file formatting it in a way to be used for next algorithms.
                #The formatting consists of the users review/opinion \t thumbsUp value \t thumbsDown value.
                #Separates a review from another by two end of lines (\n\n). 
                f_out_annot.write(opinion_str)
                f_out_annot.write("\t")
                f_out_annot.write(recommends_value)
                f_out_annot.write("\n\n\n")

                f_out.write(opinion_str)
                f_out.write("\n")
                f_out.write("MARKERENDOFREVIEW")
                f_out.write("\n\n\n")


            except IOError as exc:
                print("Erro no arquivo")
                if exc.errno != errno.EISDIR:
                    raise
            #print(name)
        f_out_annot.close()
        f_out.close()

        return annot

    #Checks line by line for the string "recommends" and return its value in the file
    def searching_recommends_value(self, file):
        line = file.readline()

        while ("recommends" not in line):
            if (len(line) != 0):
                line = file.readline()
            else:
                return

        if ("Yes" in line):
            recommends_value = "1"
        else:
            recommends_value = "-1"

        return recommends_value


    #This method search in the file for the text which have the reviewer opinion.
    #It returns a string with the opinion in the review
    def searching_opinion(self, file):
        str = file.read()
        str = str.split("<opinion>")
        str = str[1].split("</opinion>")
        str = str[0].replace("\n", " ")
        str = str.strip()
        return str


    #This method check if the first line is in the correct formatting.
    def test_formatting(self, file):
        line = file.readline()

        if ("xml version" not in line):
            #print("Arquivo", file.name, "fora de formatação\n")
            return False

        return True

    def norm_buscape(self):
        #Creates the output files clearing them, and closing.
        #This is used to not overlap data
        open(self.writefile_path, "w+", encoding="utf8").close()
        open(self.writefile_path2, "w+", encoding="utf8").close()
        
        annot = self.search_in_files(self.files, self.writefile_path, self.writefile_path2)

        print("CONCLUIDO Buscape:\n")
        print("Reviews: ", self.review_counter, "\n")
        print("Pos: ", self.pos_counter, "\n")
        print("Neg: ", self.neg_counter, "\n\n")

        return annot