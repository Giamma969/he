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
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the column "Schema di crittografia" and merge
df1_dropped = df1[['Schema di crittografia']]
df2_dropped = df2[['Schema di crittografia']]
df_merged = df1_dropped.append(df2_dropped)

#take schemes
schemes = list(df_merged['Schema di crittografia'])
schemes_cleaned = list()

#separate multivalued elements and remove inconsistent elements
for s in schemes :
    #separate multivalued elements
    if (type(s) != float and s.find(',') >= 0) :
        s_temp=s.split(', ')
        for elem in s_temp :
            schemes_cleaned.append(elem)
    #otherwise add if not consistent
    elif (type(s) != float):
        schemes_cleaned.append(s)

#create dictionary to count occurrences of schemes
dict_schemes = dict()
for s in schemes_cleaned :
    dict_schemes[s] = dict_schemes.get(s, 0) + 1


#sort dictionary for value
sorted_s = dict( sorted(dict_schemes.items(), key=operator.itemgetter(1)))

print(sorted_s)

names = list(sorted_s.keys())
values = list(sorted_s.values())

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
plt.xlim(0,55)
plt.xticks(np.arange(0,55,5), fontsize=textsize - 1)
plt.yticks(fontsize=textsize)
plt.xlabel("Numero applicazioni (%)", fontsize=textsize + 1)
plt.ylabel("Schemi", fontsize=textsize + 1)

# Add text on bars
for i, (v, p) in enumerate(zip(values, ratios)):
    plt.text(v + 0.35, r1[i] - 0.3, "{} ({}%)".format(str(v),str(p)), size = textsize)

plt.tight_layout()

#save figure
plt.savefig('../data/figures/schemes.pdf')