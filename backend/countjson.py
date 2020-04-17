import json

pathTables = 'app/test/data/tablas/tabla'
pathTexts  = 'app/test/data/textos/carta'
pathWeb    = 'app/test/data/web/web'


count = 0
for index in range(1,11):
    with open(pathWeb + "%s.json" %(index)) as file:
        data = json.load(file)
    count += len(data['names'])

print(count)