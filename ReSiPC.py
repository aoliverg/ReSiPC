import codecs
import re
import sys
import xlsxwriter
import argparse

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
    entrada=codecs.open(args.patternsfile,"r",encoding="utf-8")
    regexps=[]
    for linia in entrada:
        linia=linia.rstrip()
        regexp=translate_linguistic_pattern(linia)
        regexps.append(regexp)
    entrada.close()
    if not args.outfile.endswith(".xlsx"):
        args.outfile=args.outfile+".xlsx"
    workbook = xlsxwriter.Workbook(args.outfile)
    sheetAll = workbook.add_worksheet("All")
    sheetAll.set_column(0, 11, 50)
    bold   = workbook.add_format({'bold': True})
    normal = workbook.add_format({'bold': False})
    text_wrap = workbook.add_format({'text_wrap': 1, 'valign': 'top'})
    entrada=codecs.open(args.paracorpusfile,"r",encoding="utf-8")
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

         
            
        
    
        
    
    

parser = argparse.ArgumentParser(description='ReSiPC: a tool for searching POS patterns in tagged parallel corpora.')
parser.add_argument('-i','--in', action="store", dest="paracorpusfile", help='The input file containing the parallel corpus in tabbed text format.',required=True)
parser.add_argument('-o','--out', action="store", dest="outfile", help='The output Excel file.',required=True)
parser.add_argument('-p','--patterns', action="store", dest="patternsfile", help='The text file containing the patterns.',required=True)

args = parser.parse_args()



go()

'''
entrada=codecs.open("SHUFFLE RomCro 1-27 SE s oznakama_NOVO_TAGGED.csv","r",encoding="utf-8")

workbook = xlsxwriter.Workbook("RomCro-pasivos-spa.xlsx")
sheetAll = workbook.add_worksheet("All")
sheetAll.set_column(0, 11, 50)
#bold   = workbook.add_format({'font_name':'Tahoma', 'bold': True, 'font_size':14})
#normal = workbook.add_format({'font_name':'Tahoma', 'font_size':11})
bold   = workbook.add_format({'bold': True})
normal = workbook.add_format({'bold': False})
text_wrap = workbook.add_format({'text_wrap': 1, 'valign': 'top'})

#lema ser + etiqueta vmp.
patron="|ser| ||vmp."

expreg=translate_linguistic_pattern(patron)


cont=1
for linea in entrada:
    linea=linea.rstrip()
    campos=linea.split("\t")
    try:
        textoES=campos[0]
    except:
        textoES=""
    try:
        taggedES=campos[1]
    except:
        taggedES=""

    try:
        textoHR=campos[2]
    except:
        textoHR=""
    try:
        taggedHR=campos[3]
    except:
        taggedHR=""
    
    try:
        textoFR=campos[4]
    except:
        textoFR=""
    try:
        taggedFR=campos[5]
    except:
        taggedFR=""    
        
    try:
        textoIT=campos[6]
    except:
        textoIT=""
    try:
        taggedIT=campos[7]
    except:
        taggedIT=""
        
    try:
        textoPT=campos[8]
    except:
        textoPT=""
    try:
        taggedPT=campos[9]
    except:
        taggedPT=""
    try:
        textoRO=campos[10]
    except:
        textoRO=""
    try:
        taggedRO=campos[11]
    except:
        taggedRO=""
        
    
        
    matches = re.findall(expreg, taggedES)    
    
    if len(matches)>0:
        textoabuscar=[]
        for match in matches:
            buscar=[]
            for token in match.split(" "):
                campos2=token.split("|")
                buscar.append(campos2[0])
            buscar=" ".join(buscar)
            textoabuscar.append(buscar)
         
                
        
       
        ###
        starts=[]
        ends=[]
        intervals=[]
        for texto in textoabuscar:
            start=textoES.find(texto)
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
            segmentBOLD.append("".join(textoES[position:start]))
            segmentBOLD.append(bold)
            segmentBOLD.append("".join(textoES[start:end]))
            position=end
        segmentBOLD.append(normal)
        segmentBOLD.append("".join(textoES[position:len(textoES)]))
        ###
        #segmentBOLD="".join(segmentBOLD)        
        sheetAll.write_rich_string(cont, 0, *segmentBOLD, text_wrap)
        #sheetAll.write(cont, 1, taggedES, text_wrap)
        starts=[]
        ends=[]
        intervals=[]
        sheetAll.write(cont, 1, taggedES, text_wrap)
        try:
            for texto in matches:
                start=taggedES.find(texto)
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
                segmentBOLD.append("".join(taggedES[position:start]))
                segmentBOLD.append(bold)
                segmentBOLD.append("".join(taggedES[start:end]))
                position=end
            segmentBOLD.append(normal)
            segmentBOLD.append("".join(taggedES[position:len(taggedES)]))
            ###
            #segmentBOLD="".join(segmentBOLD)        
            sheetAll.write_rich_string(cont, 1, *segmentBOLD, text_wrap)
        except:
            sheetAll.write(cont, 1, taggedES, text_wrap)
        
        sheetAll.write(cont, 2, textoHR, text_wrap)
        sheetAll.write(cont, 3, taggedHR, text_wrap)
        
        sheetAll.write(cont, 4, textoFR, text_wrap)
        sheetAll.write(cont, 5, taggedFR, text_wrap)
        
        sheetAll.write(cont, 6, textoIT, text_wrap)
        sheetAll.write(cont, 7, taggedIT, text_wrap)
        
        sheetAll.write(cont, 8, textoPT, text_wrap)
        sheetAll.write(cont, 9, taggedPT, text_wrap)
        
        sheetAll.write(cont, 10, textoRO, text_wrap)
        sheetAll.write(cont, 11, taggedRO, text_wrap)
        
        cont+=1
        
workbook.close()
    
'''