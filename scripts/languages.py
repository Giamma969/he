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

#Extract the column "Linguaggio" and merge
df1_dropped = df1[['Linguaggio']]
df2_dropped = df2[['Linguaggio']]
df_merged = df1_dropped.append(df2_dropped)

#take languages
languages = list(df_merged['Linguaggio'])
languages_cleaned = list()

#separate multivalued elements and remove inconsistent elements
for l in languages :
    #separate multivalued elements
    if (type(l) != float and l.find(',') >= 0) :
        l_temp=l.split(', ')
        for elem in l_temp :
            languages_cleaned.append(elem)
    #otherwise add if not consistent
    elif (type(l) != float):
        languages_cleaned.append(l)


#create dictionary to count occurrences of languages
dict_l = dict()
for l in languages_cleaned :
    dict_l[l] = dict_l.get(l, 0) + 1


#sort dictionary for value
sorted_d = dict( sorted(dict_l.items(), key=operator.itemgetter(1), reverse=True))



names = list(sorted_d.keys())
values = list(sorted_d.values())

hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))
r1 = [x for x in r1]
r2 = [x + (barWidth /len(names)) for x in r1]



#plot
plt.bar(names, values, width=barWidth, alpha=0.8)
# plt.title("Linguaggi utilizzati")
plt.xticks(fontsize=textsize)
plt.yticks(fontsize=textsize)
plt.ylabel("Numero di utilizzi")
plt.xlabel("Linguaggio")
plt.axis(ymin=0, ymax=65)

#insert total for each language
for i,v in enumerate(values):
    if v<10 : 
        plt.text(r1[i] - 0.05, v + 0.3, "{}".format(str(v)), size = textsize)
    else :
        plt.text(r1[i] - 0.1, v + 0.3, "{}".format(str(v)), size = textsize)  

plt.tight_layout()

#save figure
plt.savefig('../data/figures/languages.pdf')