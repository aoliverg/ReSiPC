import stanza
import re
import codecs
import argparse
import sys

def load_taggers(l1,l2):
    try:
        nlp1 = stanza.Pipeline(l1, processors='tokenize, pos, lemma')
    except:
        print("ERROR downloading models for language ",l1)
        sys.exit()
    try:
        if not l2==None:
            nlp2 = stanza.Pipeline(l2, processors='tokenize, pos, lemma')
        else:
            nlp2=None
    except:
        print("ERROR downloading models for language ",l2)
        sys.exit()
    return(nlp1,nlp2)

def tag_corpus(nlp1,nlp2,paracorpusfile,taggedcorpusfile):
    entrada=codecs.open(paracorpusfile,"r",encoding="utf-8")
    sortida=codecs.open(taggedcorpusfile,"w",encoding="utf-8")
    for linia in entrada:
        linia=linia.rstrip()
        camps=linia.split("\t")
        try:
            sl1=camps[0]
            sl2=camps[1]
            
            doc1 = nlp1(sl1)
            taggeddoc=[]
            for sent in doc1.sentences:
                taggedsentence=[]
                for w in sent.words:
                    tokeninfo=w.text+"|"+str(w.lemma)+"|"+str(w.xpos)
                    taggedsentence.append(tokeninfo)
                taggedsentence=" ".join(taggedsentence)
                taggeddoc.append(taggedsentence)
            taggedl1=" ".join(taggeddoc)
            
            if not nlp2==None:
                doc2 = nlp2(sl2)
                taggeddoc=[]
                for sent in doc2.sentences:
                    taggedsentence=[]
                    for w in sent.words:
                        tokeninfo=w.text+"|"+str(w.lemma)+"|"+str(w.xpos)
                        taggedsentence.append(tokeninfo)
                    taggedsentence=" ".join(taggedsentence)
                    taggeddoc.append(taggedsentence)
                taggedl2=" ".join(taggeddoc)
            else:
                taggedl2=sl2
            
            cadena=sl1+"\t"+taggedl1+"\t"+sl2+"\t"+taggedl2
            print(cadena)
            sortida.write(cadena+"\n")
            
            
        except:
            print("ERRROR:",sys.exc_info())
    

parser = argparse.ArgumentParser(description='ReSiPC tagger for parallel corpora.')
parser.add_argument('-i','--in', action="store", dest="paracorpusfile", help='The input file containing the parallel corpus in tabbed text format.',required=True)
parser.add_argument('-o','--out', action="store", dest="taggedcorpusfile", help='The output file to store the tagged corpus.',required=True)
parser.add_argument('--l1', action="store", dest="L1", help='The 2 letter ISO code for language 1 (en, es, fr, ....).',required=True)
parser.add_argument('--l2', action="store", dest="L2", help='The 2 letter ISO code for language 2 (en, es, fr, ....) or None if no tagger is available.',required=True)

args = parser.parse_args()

paracorpusfile=args.paracorpusfile
taggedcorpusfile=args.taggedcorpusfile
l1=args.L1
l2=args.L2
if l2=="None":l2=None

(nlp1,nlp2)=load_taggers(l1,l2)
tag_corpus(nlp1,nlp2,paracorpusfile,taggedcorpusfile)
