import codecs
import re
import sys
import xlsxwriter
from tkinter import *
from tkinter.ttk import *

import tkinter 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox

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

def go():
    patternsfile=E2.get()
    entrada=codecs.open(patternsfile,"r",encoding="utf-8")
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
    sheetAll = workbook.add_worksheet("All")
    sheetAll.set_column(0, 11, 50)
    bold   = workbook.add_format({'bold': True})
    normal = workbook.add_format({'bold': False})
    text_wrap = workbook.add_format({'text_wrap': 1, 'valign': 'top'})
    paracorpusfile=E1.get()
    entrada=codecs.open(paracorpusfile,"r",encoding="utf-8")
    cont=1
    for linia in entrada:
        linia=linia.rstrip()
        camps=linia.split("\t")
        try:
            textL1=camps[0]
        except:
            textL1=""
        try:
            taggedL1=camps[1]
        except:
            taggedL1=""
        try:
            textL2=camps[2]
        except:
            textL2=""
        try:
            taggedL2=camps[3]
        except:
            taggedL2=""
        for expreg in regexps:
            matches = re.findall(expreg, taggedL1)
            if len(matches)>0:
                textoabuscar=[]
                for match in matches:
                    buscar=[]
                    for token in match.split(" "):
                        camps2=token.split("|")
                        buscar.append(camps2[0])
                    buscar=" ".join(buscar)
                    textoabuscar.append(buscar)
                    
                    
                starts=[]
                ends=[]
                intervals=[]
                for texto in textoabuscar:
                    start=textL1.find(texto)
                    end=start+len(texto)
                    starts.append(start)
                    ends.append(end)
                    intervals.append((start,end))
                segmentBOLD=list([])
                position=0
                for interval in intervals:
                    start=interval[0]
                    end=interval[1]
                    segmentBOLD.append(normal)
                    segmentBOLD.append("".join(textL1[position:start]))
                    segmentBOLD.append(bold)
                    segmentBOLD.append("".join(textL1[start:end]))
                    position=end
                segmentBOLD.append(normal)
                segmentBOLD.append("".join(textL1[position:len(textL1)]))
                sheetAll.write_rich_string(cont, 0, *segmentBOLD, text_wrap)
                starts=[]
                ends=[]
                intervals=[]
                sheetAll.write(cont, 1, taggedL1, text_wrap)
                try:
                    for texto in matches:
                        start=taggedL1.find(texto)
                        end=start+len(texto)
                        starts.append(start)
                        ends.append(end)
                        intervals.append((start,end))
                    segmentBOLD=list([])
                    position=0
                    for interval in intervals:
                        start=interval[0]
                        end=interval[1]
                        segmentBOLD.append(normal)
                        segmentBOLD.append("".join(taggedL1[position:start]))
                        segmentBOLD.append(bold)
                        segmentBOLD.append("".join(taggedL1[start:end]))
                        position=end
                    segmentBOLD.append(normal)
                    segmentBOLD.append("".join(taggedL1[position:len(taggedL1)]))
            
                    sheetAll.write_rich_string(cont, 1, *segmentBOLD, text_wrap)
                except:
                    sheetAll.write(cont, 1, taggedL1, text_wrap)

                sheetAll.write(cont, 2, textL2, text_wrap)
                sheetAll.write(cont, 3, taggedL2, text_wrap)
                cont+=1
    workbook.close()

         
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

B4=tkinter.Button(top, text = str("Go!"), borderwidth = 1, command=go,width=25).grid(sticky="W",row=4,column=0)

top.mainloop() 
    

