import requests
import time

nIter = 10
messure = 0
for _ in range(nIter):    
    with open('/home/miguel/Escritorio/Ingeniería informática/cuarto/TFG/utilidades/nba.xls', 'rb') as f:
        st = time.time()
        r = requests.post('http://127.0.0.1:5000/search/file/encode', files={'file': f})
        messure += time.time() - st
print(messure/nIter, "s")