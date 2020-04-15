import json

with open('/home/miguel/Escritorio/Ingeniería informática/cuarto/TFG/NameSearcher-WebService/backend/app/test/data/web/web4.json') as f:
  data = json.load(f)

for name in sorted(list(set(data['names']))):
    print(name, data['names'].count(name))