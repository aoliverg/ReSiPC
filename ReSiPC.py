import codecs
import sys
from nltk.util import ngrams
import re
import argparse
import subprocess

#Copyright: Antoni Oliver (2018)
#version 2018-09-16

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

def translate_linguistic_pattern(lp):
      
    aux=[]
    for ptoken in lp.split(" "):
        if ptoken.startswith("*"):
            tp=ptoken
            tp=tp.replace("*","([^\s]+?\|[^\s]+?\|[^\s]+?)")
            aux.append(tp)
        else:
            auxtoken=[]
            for pelement in ptoken.split("|"):                    
                if pelement=="":
                    auxtoken.append("[^\s]+?")
                else:
                    auxtoken.append(pelement)
            aux.append("\|".join(auxtoken))
            tp="("+"\s?".join(aux)+")"
    return(tp)

def translate_linguistic_pattern_noval(pattern):
       
    aux=[]
    for ptoken in pattern.split(" "):
        auxtoken=[]
        ptoken=ptoken.replace(".*","[^\s]+") 
        if ptoken.startswith("*"):
                tp=ptoken
                tp=tp.replace("*","([^\s]+?\|[^\s]+?\|[^\s]+?)")
                aux.append(tp)
        else:
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
    #tpatterns.append(tp)
    return(tp) 

def lensort(a):
    n = len(a)
    for i in range(n):
        for j in range(i+1,n):
            if len(a[i].split(" ")) > len(a[j].split(" ")):
                temp = a[i]
                a[i] = a[j]
                a[j] = temp
    return a

parser = argparse.ArgumentParser(description='ReSiPC: Regular Expressions Search in Parallel Corpora')

parser.add_argument('--st', action="store", dest="stfiles",help='The file containing the source text')
parser.add_argument('--tt', action="store", dest="ttfiles",help='The file containing the target text')
parser.add_argument('--tst', action="store", dest="tstfiles",help='The file containing the tagged source text')
parser.add_argument('--ttt', action="store", dest="tttfiles",help='The file containing the tagged target text')#The tagged target text is not used in this version of the programm
parser.add_argument('--tsv', action="store", dest="tsvfiles",help='The file containing the tab txt file')
parser.add_argument('--patterns', action="store", dest="patternsfile",required=False,help='The file containing the patterns to search')
parser.add_argument('--output', action="store", dest="outputfile",required=True,help='The output file')
parser.add_argument('--limit', action="store", dest="limit",required=False,help='The maximum number of examples for each book')
parser.add_argument('--tag_freeling_server', action="store", dest="port",required=False,help='tags the source text (--st) with a Freeling server server:port must be given')
parser.add_argument('--tag_freeling_api', action="store", dest="apipath",required=False,help='The path to the Freeling api')
parser.add_argument('--freeling_api_lang', action="store", dest="apilang",required=False,help='The lang code to start the Freeling api')




args = parser.parse_args()

resultatfinal={}
searchtaskperformed=False

patterns=[]
tpatterns=[]
if not args.patternsfile==None:
    fpatterns=codecs.open(args.patternsfile,"r",encoding="utf-8")

    for linia in fpatterns:
        linia=linia.rstrip()
        if len(linia)>0:
            patterns.append(linia)
            tpatterns.append(translate_linguistic_pattern(linia))

tpatternscomp={}
for tp in tpatterns:
    print("TP",tp)
    p = re.compile(tp).search
    tpatternscomp[tp]=p

for pattern in patterns:
    resultatfinal[pattern]=[]

equivalencia={}
for i in range(0,len(patterns)):
    equivalencia[tpatterns[i]]=patterns[i]
    
if not args.tsvfiles==None:
    for tsvfile in args.tsvfiles.split(":"):
        libro=codecs.open(tsvfile,"r",encoding="utf-8")
        ejemplos={}
        for linia in libro:
            linia=linia.strip()
            try:
                camps0=linia.split("\t")
                l1=camps0[0]
                if len(camps0)>=3:
                    l1tagged=camps0[1]
                    l2=camps0[2]
                else:
                    l1tagged=""
                    l2tagged=""
                for tp in tpatterns:
                    p=tpatternscomp[tp]
                    trobats=p(l1tagged)
                    if not trobats==None:
                        cadena=l1+"\t"+l2
                        print(cadena)
                        if equivalencia[tp] in ejemplos:
                            ejemplos[equivalencia[tp]].append(cadena)
                        else:
                            ejemplos[equivalencia[tp]]=[cadena]
                    
            except:
                print("ERROR",sys.exc_info())
                sys.exit()

        for pattern in patterns:
            if pattern in ejemplos:
                tosort=[]
                hashsort={}
                for ejemplo in ejemplos[pattern]:
                    (l1,l2)=ejemplo.split("\t")
                    tosort.append(l1)
                    hashsort[l1]=l2

                cont=0
                for l1sorted in lensort(tosort):
                    lenl1sorted=len(l1sorted.split(" "))
                    if lenl1sorted>4:
                        cont+=1
                        cadena=tsvfile+"\t"+l1sorted+"\t"+hashsort[l1sorted]
                        resultatfinal[pattern].append(cadena)
                        if cont==args.limit:
                            break
    searchtaskperformed=True

if not args.stfiles==None and not args.ttfiles==None and not args.tstfiles==None:
    stfilesl=args.stfiles.split(":")
    ttfilesl=args.ttfiles.split(":")
    tstfilesl=args.tstfiles.split(":")
    for i in range(0,len(stfilesl)):
        entrada_st=codecs.open(stfilesl[i],"r",encoding="utf-8")
        entrada_tt=codecs.open(ttfilesl[i],"r",encoding="utf-8")
        entrada_tst=codecs.open(tstfilesl[i],"r",encoding="utf-8") 
        ejemplos={}
        while 1:
            l1=entrada_st.readline().strip()
            if not l1:
                break
            l2=entrada_tt.readline().strip()
            l1tagged=entrada_tst.readline().strip()
            
            
            for tp in tpatterns:
                    p=tpatternscomp[tp]
                    trobats=p(l1tagged)
                    if not trobats==None:
                        cadena=l1+"\t"+l2
                        print(cadena)
                        if equivalencia[tp] in ejemplos:
                            ejemplos[equivalencia[tp]].append(cadena)
                        else:
                            ejemplos[equivalencia[tp]]=[cadena]
                    
            

        for pattern in patterns:
            if pattern in ejemplos:
                tosort=[]
                hashsort={}
                for ejemplo in ejemplos[pattern]:
                    (l1,l2)=ejemplo.split("\t")
                    tosort.append(l1)
                    hashsort[l1]=l2

                cont=0
                for l1sorted in lensort(tosort):
                    lenl1sorted=len(l1sorted.split(" "))
                    if lenl1sorted>4:
                        cont+=1
                        cadena=stfilesl[i]+"\t"+l1sorted+"\t"+hashsort[l1sorted]
                        resultatfinal[pattern].append(cadena)
                        if cont==args.limit:
                            break
    searchtaskperformed=True
   
if not args.port==None and not args.stfiles==None:
    sortida=codecs.open(args.outputfile,"w",encoding="utf-8")
    if args.port.find(":")>-1:
        (server,port)=args.port.split(":")
    else:
        server="localhost"
        port=args.port
    for stfile in args.stfiles.split(":"):    
        entrada=codecs.open(stfile,"r",encoding="utf-8")
        for linia in entrada:
            linia=linia.strip()
            tagdefarr=[]
            p = subprocess.Popen("echo \""+str(shlex.quote(linia))+"\" | analyzer_client "+ str(port), shell=True, stdout=subprocess.PIPE)
            out= p.communicate()
            tokens=[]
            analisis=out[0].splitlines()
            for ana in analisis:
                camps=ana.split()
                if len(camps)>=3:
                    forma=camps[0].decode("utf-8")
                    lema=camps[1].decode("utf-8")
                    tag=camps[2].decode("utf-8")
                    cadena=str(forma)+"|"+str(lema)+"|"+str(tag)
                    tagdefarr.append(cadena)
            tagged=" ".join(tagdefarr)
            sortida.write(tagged+"\n")
        
if not args.apipath==None and not args.stfiles==None:
    #sys.path.append(args.apipath)
    #import freeling
    if args.apilang==None:
        print("The language code to start the Freeling api must be given")
        sys.exit()
    LANG=args.apilang
    try:
        sys.path.append(args.apipath)
        import freeling
        FREELINGDIR = "/usr/local";
        DATA = FREELINGDIR+"/share/freeling/";
    except:
        print("No Freeling API available. Verify Freeling PATH: "+args.apipath)
        sys.exit()
    freeling.util_init_locale("default");

    # create language analyzer
    la1=freeling.lang_ident(DATA+"common/lang_ident/ident.dat");

    # create options set for maco analyzer. Default values are Ok, except for data files.
    op1= freeling.maco_options("ca");
    op1.set_data_files( "", 
                       DATA + "common/punct.dat",
                       DATA + LANG + "/dicc.src",
                       DATA + LANG + "/afixos.dat",
                       "",
                       DATA + LANG + "/locucions.dat", 
                       DATA + LANG + "/np.dat",
                       DATA + LANG + "/quantities.dat",
                       DATA + LANG + "/probabilitats.dat");

    # create analyzers
    tk1=freeling.tokenizer(DATA+LANG+"/tokenizer.dat");
    sp1=freeling.splitter(DATA+LANG+"/splitter.dat");
    sid1=sp1.open_session();
    mf1=freeling.maco(op1);

    # activate mmorpho odules to be used in next call
    mf1.set_active_options(False, True, True, False,  # select which among created 
                          True, True, False, True,  # submodules are to be used. 
                          True, True, True, True ); # default: all created submodules are used

    # create tagger, sense anotator, and parsers
    tg1=freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2);
    sortida=codecs.open(args.outputfile,"w",encoding="utf-8")
    for stfile in args.stfiles.split(":"):    
        entrada=codecs.open(stfile,"r",encoding="utf-8")
        for linia in entrada:
            linia=linia.strip()
            l1 = tk1.tokenize(linia);
            ls1 = sp1.split(sid1,l1,True);
            ls1 = mf1.analyze(ls1);
            ls1 = tg1.analyze(ls1);
            ttsentence=[]
            for s in ls1 :
              ws = s.get_words();
              for w in ws :
                form=w.get_form()
                lemma=w.get_lemma()
                tag=w.get_tag()
                #print(form,lemma,tag)        
                ttsentence.append(form+"|"+lemma+"|"+tag)
            ttsentence=" ".join(ttsentence)
            sortida.write(ttsentence+"\n")
    
if searchtaskperformed:
    sortida=codecs.open(args.outputfile,"w",encoding="utf-8")
    control={}
    for pattern in patterns:
        for resultat in resultatfinal[pattern]:
            cadena=pattern+"\t"+resultat
            if not cadena in control:
                print(cadena)
                sortida.write(cadena+"\n")
                control[cadena]=1
