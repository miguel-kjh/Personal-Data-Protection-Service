import requests
import time

nIter = 10
messure = 0
listaNames = 'http://127.0.0.1:5000/search/file/list-names'
encode = 'http://127.0.0.1:5000/search/file/encode'
file = 'demos/lista_alumnos.pdf'

for _ in range(nIter):    
    with open(file, 'rb') as f:
        st = time.time()
        r = requests.post(listaNames, files={'file': f})
        messure += time.time() - st
print(messure/nIter, "s")