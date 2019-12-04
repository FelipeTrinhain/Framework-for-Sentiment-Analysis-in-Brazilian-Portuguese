import subprocess

p1 = subprocess.Popen(["perl",
                      "D:\\TreeTagger\\cmd\\utf8-tokenize.perl", "-e", "-a",
                     "D:\\TreeTagger\\lib\\portuguese-abbreviations.txt", "D:\\Users\\Felipe\\Documents\\Projects\\Python Projects\\Reviews_corpus_buscape\\out.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


p2 = subprocess.Popen(["D:\\TreeTagger\\bin\\tree-tagger.exe", "D:\\TreeTagger\\lib\\pt.par", "-token", "-lemma", "-sgml"], stdin=p1.stdout, stdout=subprocess.PIPE)

stdout, stderr = p2.communicate()

with open("D:\\TreeTagger\\cmd\\saida.txt", "w") as f:
    f.write(stdout.decode(encoding="utf8", errors="ignore"))