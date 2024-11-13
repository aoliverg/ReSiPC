import codecs
import re
import sys
import xlsxwriter
import argparse

from tkinter import *
from tkinter.ttk import *

import tkinter 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox

def remove_xml_tags_and_retrieve(text):
    """
    Removes XML tags from a given string and retrieves the deleted tags.

    Args:
        text (str): The input string containing XML tags.

    Returns:
        tuple: A tuple containing the cleaned string and a list of deleted tags.
    """
    # Regular expression to match XML tags
    tag_re = re.compile(r'<[^>]+>')
    
    # Find all tags in the text
    tags = tag_re.findall(text)
    
    # Remove all tags from the text
    cleaned_text = tag_re.sub('', text)
    
    return cleaned_text.rstrip().lstrip(), tags

def translate_linguistic_pattern(pattern):
        aux=[]
        for ptoken in pattern.split():
            auxtoken=[]
            ptoken=ptoken.replace(".*","[^\s]+") 
            for pelement in ptoken.split("|"):
                if pelement=="#":
                    auxtoken.append("([^\s]+?)")                    
                elif pelement=="":
                    auxtoken.append("[^\s]+?")
                else:
                    if pelement.startswith("#"):
                        auxtoken.append("("+pelement.replace("#","")+")")
                    else:
                        auxtoken.append(pelement)
            aux.append("\|".join(auxtoken))
        tp="("+" ".join(aux)+")"
        return(tp)

def getWordForms(cadena):
    tokens=cadena.split()
    palabras=[]
    for t in tokens:
        palabras.append(t.split("|")[0])
    palabras=" "+" ".join(palabras)+" "
    return(palabras)

def go():
    
    patternfile=E2.get()
    entrada=codecs.open(patternfile,"r",encoding="utf-8")
    regexps=[]
    for linia in entrada:
        linia=linia.rstrip()
        regexp=translate_linguistic_pattern(linia)
        regexps.append(regexp)
    entrada.close()
    outfile=E3.get()
    if not outfile.endswith(".xlsx"):
        outfile=outfile+".xlsx"
    workbook = xlsxwriter.Workbook(outfile)
    bold_format = workbook.add_format({'bold': True})
    sheetAll = workbook.add_worksheet("All")
    sheetAll.set_column(0, 11, 50)
    bold   = workbook.add_format({'bold': True})
    normal = workbook.add_format({'bold': False})
    text_wrap = workbook.add_format({'text_wrap': 1, 'valign': 'top'})
    paracorpusfile=E1.get()
    entrada=codecs.open(paracorpusfile,"r",encoding="utf-8")
    cont=1
    contlinia=0
    matchedlines={}
    for linia in entrada:
        
        matchstart={}
        linia=linia.rstrip()
        camps=linia.split("\t")
        sourcecolumn=varSourceColumn.get()
        taggedcolumn=varTargetColumn.get()
        try:
            textL1ORIG=camps[sourcecolumn]
            textL1,tags=remove_xml_tags_and_retrieve(textL1ORIG)
        except:
            textL1=""
        try:
            taggedL1=camps[taggedcolumn]
        except:
            taggedL1=""

        allmatches=[]
        ignorecase=varIgnoreCase.get()
        for expreg in regexps:
            if ignorecase:
                matches = re.findall(expreg, taggedL1,re.IGNORECASE)
            else:
                matches = re.findall(expreg, taggedL1)
            if len(matches)>0:
                
                # This list will hold the parts of the rich string
                
                allmatches.extend(matches)
                
        ALLmatches=list(set(allmatches))
                #####
        if len(ALLmatches)>0:
            matchedlines[contlinia]=1
            rich_text = []
            rich_text_tags = []
            current_position = 0
            if len(tags)>0:
                rich_text.append(tags[0])        
            for match in ALLmatches:
                pattern = r'\b' + re.escape(match) + r'\b'
                matchesTagged = list(re.finditer(pattern, taggedL1))
                for matchTagged in matchesTagged:
                    start_idx = matchTagged.start()
                    end_idx = matchTagged.end()
                    #print(match,start_idx,end_idx)
                    index=str(match)+":"+str(start_idx)+":"+str(end_idx)
                    matchstart[index]=start_idx
            sorted_dict = dict(sorted(matchstart.items(), key=lambda item: item[1]))
            sheetAll.write(cont, sourcecolumn, textL1ORIG, text_wrap)
            sheetAll.write(cont, taggedcolumn, taggedL1, text_wrap)
            for info in sorted_dict:
                m=info.split(":")[0]
                start_idx=int(info.split(":")[1])
                end_idx=int(info.split(":")[2])
                # Add the text before the matched word (if any)
                if current_position < start_idx:
                    rich_text_tags.append(taggedL1[current_position:start_idx])
                    wordforms=getWordForms(taggedL1[current_position:start_idx])
                    rich_text.append(wordforms)
                
                # Add the matched word in bold
                rich_text_tags.append(bold_format)
                rich_text_tags.append(taggedL1[start_idx:end_idx])
                wordforms=getWordForms(taggedL1[start_idx:end_idx])
                rich_text.append(bold_format)
                rich_text.append(wordforms)
                
                # Update the current position
                current_position = end_idx

            # Add any remaining text after the last match
            if current_position < len(taggedL1):
                rich_text_tags.append(taggedL1[current_position:])
                wordforms=getWordForms(taggedL1[current_position:])
                rich_text.append(wordforms)

            # Write the rich string to the worksheet
            for moreinfo in range(0,sourcecolumn):
                sheetAll.write(cont, moreinfo, camps[moreinfo], text_wrap)
            if len(tags)>1:
                rich_text.append(tags[1])
            marksource=varMark.get()
            if marksource:
                sheetAll.write_rich_string(cont,sourcecolumn, *rich_text, text_wrap)
            else:
                sheetAll.write(cont, sourcecolumn, textL1ORIG, text_wrap)
            sheetAll.write_rich_string(cont,taggedcolumn, *rich_text_tags, text_wrap)
            '''
            sheetAll.write(cont, 2, textL2, text_wrap)
            sheetAll.write(cont, 3, taggedL2, text_wrap)
            '''
            for moreinfo in range(taggedcolumn+1,len(camps)):
                sheetAll.write(cont, moreinfo, camps[moreinfo], text_wrap)
            cont+=1
        contlinia+=1                
   
    workbook.close()
    entrada.close()
    #write csv with non mathed lines     
    paracorpusfile=E1.get()
    nomatchesfile=E8.get()
    if not nomatchesfile==None:
        entrada=codecs.open(paracorpusfile,"r",encoding="utf-8")
        sortida=codecs.open(nomatchesfile,"w",encoding="utf-8")
        contlinia=0
        for linia in entrada:
            linia=linia.rstrip()
            if not contlinia in matchedlines:
                sortida.write(linia+"\n")
            contlinia+=1
    
        entrada.close()
        sortida.close()
    

         
def select_input_corpus():
    paracorpusfile = askopenfilename(initialdir = ".",filetypes =(("All Files","*.*"),),
                           title = "Select the input file.")
    E1.delete(0,END)
    E1.insert(0,paracorpusfile)
    E1.xview_moveto(1)
    
def select_patterns_file():
    patternsfile = askopenfilename(initialdir = ".",filetypes =(("All Files","*.*"),),
                           title = "Select the input file.")
    E2.delete(0,END)
    E2.insert(0,patternsfile)
    E2.xview_moveto(1)
    
def select_output_file():
    outfile = asksaveasfilename(initialdir = ".",filetypes =(("Excel Files","*.xlsx"),("All Files","*.*")),
                           title = "Select the output file.")
    E3.delete(0,END)
    E3.insert(0,outfile)
    E3.xview_moveto(1)
    
def select_nomatchesfile():
    outfile = asksaveasfilename(initialdir = ".",filetypes =(("All Files","*.*"),),
                           title = "Select the nomatchesfile file.")
    E8.delete(0,END)
    E8.insert(0,outfile)
    E8.xview_moveto(1)
        
    
        
top = Tk()
top.title("ReSiPC")

B1=tkinter.Button(top, text = str("Select input corpus"), borderwidth = 1, command=select_input_corpus,width=25).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=80, justify="right")
E1.grid(row=0,column=1)

B2=tkinter.Button(top, text = str("Select patterns file"), borderwidth = 1, command=select_patterns_file,width=25).grid(row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=80, justify="right")
E2.grid(row=1,column=1)

B3=tkinter.Button(top, text = str("Select output file"), borderwidth = 1, command=select_output_file,width=25).grid(row=2,column=0)
E3 = tkinter.Entry(top, bd = 5, width=80, justify="right")
E3.grid(row=2,column=1)

varMark = tkinter.IntVar()
CB4 = tkinter.Checkbutton(top, text="Mark source", variable=varMark)
CB4.grid(row=3,column=0,sticky="W")

varIgnoreCase = tkinter.IntVar()
CB5 = tkinter.Checkbutton(top, text="Ignore case", variable=varIgnoreCase)
CB5.grid(row=4,column=0,sticky="W")

varSourceColumn= tkinter.IntVar()
varSourceColumn.set(0)
L6 = Label(top,text="Source column:").grid(sticky="E",row=5,column=0)
E6 = Entry(top, textvariable=varSourceColumn, width=5,)
E6.grid(row=5,column=1,sticky="W")

varTargetColumn= tkinter.IntVar()
varTargetColumn.set(1)
L7 = Label(top,text="Target column:").grid(sticky="E",row=6,column=0)
E7 = Entry(top, textvariable=varTargetColumn, width=5,)
E7.grid(row=6,column=1,sticky="W")

B8=tkinter.Button(top, text = str("Select nomatchesfile"), borderwidth = 1, command=select_nomatchesfile,width=25).grid(row=7,column=0)
E8 = tkinter.Entry(top, bd = 7, width=80, justify="right")
E8.grid(row=7,column=1)

B9=tkinter.Button(top, text = str("Go!"), borderwidth = 1, command=go,width=25).grid(sticky="W",row=8,column=0)



top.mainloop() 
    

