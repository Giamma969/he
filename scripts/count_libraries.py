import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the columns "Tipo Venue", "Anno", "Libreria" e "Linguaggio"
df1_dropped = df1[['Libreria']]
df2_dropped = df2[['Libreria']]

#merge dataframe
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

#group k in 'others' when value(k) <= 3
libraries_final = list()
for k,v in dict_lib.items() :
    if v <= 3 :
        for i in range(v) :
            libraries_final.append('Other')
    else :
        for i in range (v) :
            libraries_final.append(k)

dict_lib2 = dict()
for lib in libraries_final :
    dict_lib2[lib] = dict_lib2.get(lib, 0) + 1


#plot
names = list(dict_lib2.keys())
values = list(dict_lib2.values())
colors=["limegreen", "darkorange", "darkred", "grey", "blue", "purple", "black", "red", 'lightblue']

plt.title("Librerie utilizzate")
plt.xticks(np.arange(0,50,5))
fig_size = plt.rcParams["figure.figsize"]
plt.rcParams["figure.figsize"] = ['12','8']
plt.barh(names, values, height=np.full(9, 0.8), color=colors)
plt.axis(xmin=0, xmax=50)
plt.tight_layout()
# plt.grid(True, alpha=0.5)
# plt.show()
plt.savefig('../data/figures/count_libraries.pdf', format='pdf')





