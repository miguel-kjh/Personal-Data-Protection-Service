"""import json

pathTables = 'app/test/data/tablas/tabla'
pathTexts  = 'app/test/data/textos/carta'
pathWeb    = 'app/test/data/web/web'


count = 0
for index in range(1,11):
    with open(pathWeb + "%s.json" %(index)) as file:
        data = json.load(file)
    count += len(data['names'])

print(count)"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('app/test/result/web_report.csv')
block = df[(df["TYPE"] == 'False Negative') & (df["MATCHES"] > 0)].groupby('FILE').groups
block = {k:len(v) for k,v in block.items()}
print(block)

#plt.tight_layout()
plt.subplots_adjust(hspace=0.5)
plt.subplot(211)
plt.bar(block.keys(), block.values(), align='center', alpha=0.5)
#plt.xticks(len(block.keys()), block.keys())
plt.ylabel('Fails')
plt.title('xxx')

block = df[df["TYPE"] == 'False Positive'].groupby('FILE').groups
block = {k:len(v) for k,v in block.items()}
print(block)
plt.subplot(212)
plt.bar(block.keys(), block.values(), align='center', alpha=0.5)
#plt.xticks(len(block.keys()), block.keys())
plt.ylabel('Fails')
plt.title('xxx')

plt.show()