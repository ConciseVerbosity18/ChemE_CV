import re
import pandas as pd
path = r'C:\Users\zhgal\Desktop\t1g1.txt'
text = ''
with open(path,'r',encoding='utf8') as f:
    text = f.read()
patterns = [r'\n ']
replace = ['\n']
text = text.replace('(tsat/°C)\n','')

p = re.compile("\n")
indices = []
indices = [5, 10, 15, 20, 25]
# for index in indices_:
#     text = text[:index] + '_' + text[index + 1:]
for index in indices:
    text = text[:index] + ' ' + text[index + 1:]

patpres = re.compile(r'(\d{1,5})(\n)(\(\d+\.\d+\)\n)')
pressures = []

for m in patpres.finditer(text):
#     print(len(m.group()))
    new = m.groups()[0]+ '_' + m.groups()[2]
    if m.start() < 115:
#         print(new)
        text = text[:m.start()] + ' ' + new  + ' ' + text[m.start()+ len(m.group()):]
    else:
        break
for m in patpres.finditer(text):
    new = m.groups()[0] + '_' + m.groups()[2]
    pressures.append(new.replace('\n',''))
    text = text.replace(m.group(),'')
text = text[:25] + '' + text[25 + 1:]
# text = text.replace('. . . . . . ','......')
text = text.replace(' V','V')
text = re.sub(r'(\. ){6}','...... ',text)
let = [r'(?<!_)V',r'(?<!_)U',r'(?<!_)H',r'(?<!_)S']
trash = re.compile(r'TABLE E.2 Properties of Superheated Steam\nFinal PDF to printer\nAPPENDIX E. Steam Tables \d+')
for pr in pressures:
    for le in let:
        text = re.sub(re.compile(le), pr+'_' + le[-1],text,1)
text = text.replace('sat.\n','')
# text = text.replace('sat.\nvap','sat._vap')
with open(path,'w',encoding='utf8') as f:
    f.write(text)
data = pd.read_csv(path,sep=' ')
data