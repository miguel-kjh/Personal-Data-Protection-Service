import requests
import time

nIter = 10
messure = 0
listaNames = 'http://127.0.0.1:5000/search/file/extract-data/json'
encode = 'http://127.0.0.1:5000/search/file/encode'
file = '/home/miguel/Escritorio/Ingeniería informática/cuarto/TFG/NameSearcher-WebService/frontend-test/demos/prueba.html'

for _ in range(nIter):
    with open(file, 'rb') as f:
        st = time.time()
        r = requests.post(encode, files={'file': f})
        messure += time.time() - st
print(messure/nIter, "s")