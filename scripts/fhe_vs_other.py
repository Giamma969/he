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
df1 = pd.read_excel (IN_FILE, sheet_name='Selezione rivisto')
df2 = pd.read_excel (IN_FILE, sheet_name='Snowballing rivisto')

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


#group k in 'altro' if (k != FHE) and (k != HE)
types_final = list()
for elem in types_cleaned :
    if elem != 'FHE' and elem != 'HE':
        types_final.append('Altro')
    else :
        types_final.append(elem)

#new dictionary with "altro" added
dict_types = dict()
for t in types_final :
    dict_types[t] = dict_types.get(t, 0) + 1

#sort dictionary for value
sorted_d = dict( sorted(dict_types.items(), key=operator.itemgetter(1)))

print(sorted_d)

names = ['FHE','Altro','HE']
values = [73,76,45]

for i, (k,v) in enumerate(zip(names,values)) :
    plt.bar(x=k, width=barWidth, height=v,label=k, alpha=0.8)

hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))

# Add text on bars
for i,v in enumerate(values):
    if i in [0] :
        plt.text(r1[i] - 0.1, v + 1.5, "{}".format(str(v)), size = textsize)
    else :
        plt.text(r1[i] - 0.05, v + 0.7, "{}".format(str(v)), size = textsize)

# plt.title("Coinvolgimento delle industrie", fontsize=textsize + 2)
plt.axis(ymax=90)
plt.xticks(fontsize=textsize - 1)
plt.yticks(fontsize=textsize - 1)
plt.xlabel("Tipo HE", fontsize=textsize + 1)
plt.ylabel("Numero di utilizzi", fontsize=textsize + 1)
plt.legend(loc="upper right")
plt.tight_layout()

#save figure
plt.savefig('../data/figures/fhe_vs_other.pdf', format='pdf')
