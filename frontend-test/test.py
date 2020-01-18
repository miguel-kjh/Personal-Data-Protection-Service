import requests
import time

nIter = 100
messure = 0
for _ in range(nIter):    
    with open('/home/miguel/Escritorio/Ingeniería informática/cuarto/TFG/NameSearcher-WebService/frontend-test/demos/prueba_es.xls', 'rb') as f:
        st = time.time()
        r = requests.post('http://127.0.0.1:5000/search/file/list-names', files={'file': f})
        messure += time.time() - st
print(messure/nIter, "s")