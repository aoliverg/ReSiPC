import stanza
import re
import codecs
from tkinter import *
from tkinter.ttk import *

import tkinter 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import sys

def select_input_corpus():
    paracorpusfile = askopenfilename(initialdir = ".",filetypes =(("All Files","*.*"),),
                           title = "Select the input file.")
    E1.delete(0,END)
    E1.insert(0,paracorpusfile)
    E1.xview_moveto(1)
    
def select_output_corpus():
    taggedcorpusfile = asksaveasfilename(initialdir = ".",filetypes =(("All Files","*.*"),),
                           title = "Select the output file.")
    E2.delete(0,END)
    E2.insert(0,taggedcorpusfile)
    E2.xview_moveto(1)
    
def go():
    l1=EL1.get()
    l2=EL2.get()
    if l2=="None": l2=None
    paracorpusfile=E1.get()
    taggedcorpusfile=E2.get()
    (nlp1,nlp2)=load_taggers(l1,l2)
    tag_corpus(nlp1,nlp2,paracorpusfile,taggedcorpusfile)
    

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
    
top = Tk()
top.title("paraTagger")

B1=tkinter.Button(top, text = str("Select input corpus"), borderwidth = 1, command=select_input_corpus,width=25).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=80, justify="right")
E1.grid(row=0,column=1)

B2=tkinter.Button(top, text = str("Select output tagged corpus"), borderwidth = 1, command=select_output_corpus,width=25).grid(row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=80, justify="right")
E2.grid(row=1,column=1)

labelL1 = Label(top,text="Source language:",width=15)
labelL1.grid(row=2,column=0)
EL1 = tkinter.Entry(top, bd = 5, width=10, justify="left")
EL1.grid(row=2,column=1)

labelL2 = Label(top,text="Target language:",width=15)
labelL2.grid(row=3,column=0)
EL2 = tkinter.Entry(top, bd = 5, width=10, justify="left")
EL2.grid(row=3,column=1)

B3=tkinter.Button(top, text = str("POS Tag!"), borderwidth = 1, command=go,width=25).grid(sticky="W",row=4,column=0)

top.mainloop()

