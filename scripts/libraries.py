import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator

# set width of bar
barWidth = 0.5
#set text size
textsize = 10

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the column "Libreria" and merge
df1_dropped = df1[['Libreria']]
df2_dropped = df2[['Libreria']]
df_merged = df1_dropped.append(df2_dropped)

#take libraries
libraries = list(df_merged['Libreria'])
libreries_cleaned = list()

#separate multivalued elements and remove inconsistent elements
for lib in libraries :
    #separate multivalued elements
    if (type(lib) != float and lib.find(',') >= 0) :
        lib_temp=lib.split(', ')
        for elem in lib_temp :
            libreries_cleaned.append(elem)
    #otherwise add if not consistent
    elif (type(lib) != float):
        libreries_cleaned.append(lib)


#create dictionary to count occurrences of libraries
dict_lib = dict()
for lib in libreries_cleaned :
    dict_lib[lib] = dict_lib.get(lib, 0) + 1

#group k in 'altro' when value(k) <= 3
libraries_final = list()
for k,v in dict_lib.items() :
    if v <= 3 :
        for i in range(v) :
            libraries_final.append('Altro')
    else :
        for i in range (v) :
            libraries_final.append(k)

#new dictionary with "altro" added
dict_lib2 = dict()
for lib in libraries_final :
    dict_lib2[lib] = dict_lib2.get(lib, 0) + 1

#sort dictionary for value
sorted_d = dict( sorted(dict_lib2.items(), key=operator.itemgetter(1)))

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
plt.title("Librerie utilizzate")
plt.xticks(np.arange(0,65,5), fontsize=textsize)
plt.yticks(fontsize=textsize)
plt.xlabel("Numero di utilizzi (%)")
plt.ylabel("Libreria")
plt.axis(xmin=0, xmax=60)
plt.tight_layout()


#insert total and ratio for each lib 
for i, (v, p) in enumerate(zip(values, ratios)):
    plt.text(v + 0.3, r2[i] - 0.63, "{} ({}%)".format(str(v),str(p)), size = textsize)   
    

#save figure
plt.savefig('../data/figures/libraries.pdf')