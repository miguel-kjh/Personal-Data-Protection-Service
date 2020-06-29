import requests

server = "http://127.0.0.1:5000"

req = requests.post(server + "/search/file/extract-data/json?personalData=names", files = {'file': open('demos/titulares.csv','rb')})
print(req.json())