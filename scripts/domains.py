import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator


# set width of bar
barWidth = 0.7
#set text size
textsize = 7

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Selezione rivisto')
df2 = pd.read_excel (IN_FILE, sheet_name='Snowballing rivisto')

#Extract the column "Dominio" and merge
df1_dropped = df1[['Dominio']]
df2_dropped = df2[['Dominio']]
df_merged = df1_dropped.append(df2_dropped)

#take domains
domains = list(df_merged['Dominio'])
domains_cleaned = list()

#separate multivalued elements and remove inconsistent elements
for d in domains :
    #separate multivalued elements
    if (type(d) != float and d.find(',') >= 0) :
        d_temp=d.split(', ')
        for elem in d_temp :
            domains_cleaned.append(elem)
    #otherwise add if not inconsistent
    elif (type(d) != float):
        domains_cleaned.append(d)

#create dictionary to count occurrences of domains
dict_dom = dict()
for d in domains_cleaned :
    dict_dom[d] = dict_dom.get(d, 0) + 1


#sort dictionary for value
sorted_d = dict( sorted(dict_dom.items(), key=operator.itemgetter(1)))

names = list(sorted_d.keys())
values = list(sorted_d.values())

hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))
r1 = [x for x in r1]
r2 = [x + barWidth for x in r1]

#calculate ratio
total = sum(values)
ratios = list()
for v in values :
    ratios.append(round(v / total * 100,2))

#plot
plt.barh(names, values, height=barWidth, alpha=0.8)
# plt.title("Domini di applicazione", fontsize=textsize + 2)
plt.xlim(0,105)
plt.xticks(np.arange(0,115,5), fontsize=textsize - 1)
plt.yticks(fontsize=textsize)
plt.xlabel("Numero applicazioni (%)", fontsize=textsize + 1)
plt.ylabel("Domini", fontsize=textsize + 1)

# Add text on bars
for i, (v, p) in enumerate(zip(values, ratios)):
    plt.text(v + 0.35, r1[i] - 0.3, "{} ({}%)".format(str(v),str(p)), size = textsize)

plt.tight_layout()

#save figure
plt.savefig('../data/figures/domains.pdf')