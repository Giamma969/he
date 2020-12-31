import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator

# set width of bar
barWidth = 0.75
#set text size
textsize = 10

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the column "Tipo HE" and merge
df1_dropped = df1[['Tipo HE']]
df2_dropped = df2[['Tipo HE']]
df_merged = df1_dropped.append(df2_dropped)

#take HE types
types = list(df_merged['Tipo HE'])
types_cleaned = list()

#separate multivalued elements and remove inconsistent elements
for t in types :
    #separate multivalued elements
    if (type(t) != float and t.find(',') >= 0) :
        t_temp=t.split(', ')
        for elem in t_temp :
            types_cleaned.append(elem)
    #otherwise add if not consistent
    elif (type(t) != float):
        types_cleaned.append(t)


#create dictionary to count occurrences of types
dict_t = dict()
for t in types_cleaned :
    dict_t[t] = dict_t.get(t, 0) + 1

#group k in 'altro' when value(k) <= 3
types_final = list()
for k,v in dict_t.items() :
    if v <= 4 and k != 'APX-HE':
        for i in range(v) :
            types_final.append('Altro')
    else :
        for i in range (v) :
            types_final.append(k)

#new dictionary with "altro" added
dict_t2 = dict()
for t in types_final :
    dict_t2[t] = dict_t2.get(t, 0) + 1

#sort dictionary for value
sorted_d = dict( sorted(dict_t2.items(), key=operator.itemgetter(1), reverse=True))

print(sorted_d)

names = list(sorted_d.keys())
values = list(sorted_d.values())

hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))
r1 = [x for x in r1]
r2 = [x + (barWidth /len(names)) for x in r1]



#plot
plt.bar(names, values, width=barWidth, alpha=0.8)
plt.xticks(fontsize=textsize)
plt.yticks(fontsize=textsize)
plt.ylabel("Numero di utilizzi")
plt.xlabel("Tipo HE")
plt.axis(ymin=0, ymax=80)

#insert total for each language
for i,v in enumerate(values):
    if v<10 : 
        plt.text(r1[i] - 0.08, v + 0.3, "{}".format(str(v)), size = textsize)
    else :
        plt.text(r1[i] - 0.13, v + 0.3, "{}".format(str(v)), size = textsize)  

plt.tight_layout()

#save figure
plt.savefig('../data/figures/typesHE.pdf')