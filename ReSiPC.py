import codecs
import re
import sys
import xlsxwriter
import argparse

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
    bold_format = workbook.add_format({'bold': True})
    sheetAll = workbook.add_worksheet("All")
    sheetAll.set_column(0, 11, 50)
    bold   = workbook.add_format({'bold': True})
    normal = workbook.add_format({'bold': False})
    text_wrap = workbook.add_format({'text_wrap': 1, 'valign': 'top'})
    entrada=codecs.open(args.paracorpusfile,"r",encoding="utf-8")
    cont=1
    contlinia=0
    matchedlines={}
    for linia in entrada:
        
        matchstart={}
        linia=linia.rstrip()
        camps=linia.split("\t")
        try:
            textL1ORIG=camps[args.sourcecolumn]
            textL1,tags=remove_xml_tags_and_retrieve(textL1ORIG)
        except:
            textL1=""
        try:
            taggedL1=camps[args.taggedcolumn]
        except:
            taggedL1=""

        allmatches=[]
        for expreg in regexps:
            if args.ignorecase:
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
            sheetAll.write(cont, args.sourcecolumn, textL1ORIG, text_wrap)
            sheetAll.write(cont, args.taggedcolumn, taggedL1, text_wrap)
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
            for moreinfo in range(0,args.sourcecolumn):
                sheetAll.write(cont, moreinfo, camps[moreinfo], text_wrap)
            if len(tags)>1:
                rich_text.append(tags[1])
            if args.marksource:
                sheetAll.write_rich_string(cont,args.sourcecolumn, *rich_text, text_wrap)
            else:
                sheetAll.write(cont, args.sourcecolumn, textL1ORIG, text_wrap)
            sheetAll.write_rich_string(cont,args.taggedcolumn, *rich_text_tags, text_wrap)
            '''
            sheetAll.write(cont, 2, textL2, text_wrap)
            sheetAll.write(cont, 3, taggedL2, text_wrap)
            '''
            for moreinfo in range(args.taggedcolumn+1,len(camps)):
                sheetAll.write(cont, moreinfo, camps[moreinfo], text_wrap)
            cont+=1
        contlinia+=1                
   
    workbook.close()
    entrada.close()
    #write csv with non mathed lines     
    
    if not args.nomatchesfile==None:
        entrada=codecs.open(args.paracorpusfile,"r",encoding="utf-8")
        sortida=codecs.open(args.nomatchesfile,"w",encoding="utf-8")
        contlinia=0
        for linia in entrada:
            linia=linia.rstrip()
            if not contlinia in matchedlines:
                sortida.write(linia+"\n")
            contlinia+=1
    
        entrada.close()
        sortida.close()
    
            
        
    
        
    
    

parser = argparse.ArgumentParser(description='ReSiPC: a tool for searching POS patterns in tagged parallel corpora.')
parser.add_argument('-i','--in', action="store", dest="paracorpusfile", help='The input file containing the parallel corpus in tabbed text format.',required=True)
parser.add_argument('-o','--out', action="store", dest="outfile", help='The output Excel file.',required=True)
parser.add_argument('-p','--patterns', action="store", dest="patternsfile", help='The text file containing the patterns.',required=True)
parser.add_argument('-m','--marksource', action="store_true", dest="marksource", help='Mark in bold the matches in source text (result is tokenized).',required=False, default=False)
parser.add_argument('-c','--ignorecase', action="store_true", dest="ignorecase", help='Ignore case in matching regular expressions.',required=False, default=False)
parser.add_argument('-s','--source', action="store", dest="sourcecolumn", help='The column storing the source text (0 is first). Default 0.',required=False, default=0, type=int)
parser.add_argument('-t','--tagged', action="store", dest="taggedcolumn", help='The column storing the tagged (0 is first). Default 1',required=False, default=1, type=int)
parser.add_argument('-n','--nomatches', action="store", dest="nomatchesfile", help='A tsv file to store the lines not matching any pattern.',required=False)

args = parser.parse_args()



go()
