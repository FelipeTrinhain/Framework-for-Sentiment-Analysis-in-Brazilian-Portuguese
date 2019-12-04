#!/usr/bin/python
import errno
import os


class POSTagger:

    def __init__(self):
        self.temp_path = '/mnt/d/Users/Felipe/Documents/Projects/Python Projects/tempReview.txt'
        

    def open_temp_file(self, review):
        try:
            f = open(self.temp_path, "w+", encoding="utf8")
            f.write(review)
            f.close()

        except IOError as exc:
            print("Erro no arquivo")
            if exc.errno != errno.EISDIR:
                raise

    def freeling(self, review):
        self.open_temp_file(review)
        cmd = 'analyze -f pt.cfg < /mnt/d/Users/Felipe/Documents/Projects/Python\ Projects/tempReview.txt > /mnt/d/TreeTagger/cmd/tree-tagger-portuguese > /mnt/d/Users/Felipe/Documents/Projects/Python\ Projects/saidaFreeling.txt'
        os.system(cmd)

    def freeling2(self):
        #self.open_temp_file(review)
        cmd = 'analyze -f pt.cfg < /mnt/d/Users/Felipe/Documents/Projects/Python\ Projects/Reviews_corpus_buscape/out.txt > /mnt/d/TreeTagger/cmd/tree-tagger-portuguese > /mnt/d/Users/Felipe/Documents/Projects/Python\ Projects/saidaFreeling.txt'
        os.system(cmd)

    def linguakit(self, review):
        self.open_temp_file(review)
        cmd = '~/Linguakit-master/linguakit tagger pt /mnt/d/Users/Felipe/Documents/Projects/Python\ Projects/tempReview.txt > /mnt/d/TreeTagger/cmd/tree-tagger-portuguese > /mnt/d/Users/Felipe/Documents/Projects/Python\ Projects/saidaLinguakit.txt'
        os.system(cmd)

    def treetagger(self, review):
        #self.open_temp_file(review)
        cmd = 'cat /mnt/d/Users/Felipe/Documents/Projects/Python\ Projects/tempReview.txt | /mnt/d/TreeTagger/cmd/tree-tagger-portuguese > /mnt/d/Users/Felipe/Documents/Projects/Python\ Projects/saidaTTag.txt'
        os.system(cmd)

#pos_tag = POSTagger()
#pos_tag.freeling2()