import requests

with open('demos/lista_alumnos.docx', 'rb') as f:
    r = requests.post('http://127.0.0.1:5000/file/giveCsvFile', files={'file': f})
print(r.text)