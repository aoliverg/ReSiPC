import sys
import os

langcode=sys.argv[1]
port=sys.argv[2]

comanda="analyze -f "+langcode+".cfg +  --server --port "+str(port)+" &"

os.system(comanda)
