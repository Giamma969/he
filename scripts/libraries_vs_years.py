import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator

#separate multivalued elements and remove inconsistent elements
def clean(libraries) :
    libraries_cleaned = list()
    for lib in libraries :
        #separate multivalued elements
        if (type(lib) != float and lib.find(',') >= 0) :
            lib_temp=lib.split(', ')
            for elem in lib_temp :
                libraries_cleaned.append(elem)
        #otherwise add if not consistent
        elif (type(lib) != float):
            libraries_cleaned.append(lib)
    return libraries_cleaned

#retrieve a dictionary for libraries
def dict_lib(libraries) :
    d = dict()
    for lib in libraries :
        d[lib] = d.get(lib, 0) + 1
    return d

#group less important libraries in 'altro' 
def group(d1) :
    l = list()
    for k,v in d1.items() :
        if k in ['Cingulata','Gazelle','GMP', 'ABY','FHEW','PySEAL'] :
            for i in range(v) :
                l.append('Altro')
        else :
            for i in range (v) :
                l.append(k)
    #new dictionary with "altro" added
    d2 = dict()
    for lib in l :
        d2[lib] = d2.get(lib, 0) + 1
    return d2



#set text size
textsize = 7

#set bar width
barWidth = 0.75

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the columns "Libreria","Anno" and merge
df1_dropped = df1[['Libreria','Anno']]
df2_dropped = df2[['Libreria','Anno']]
df_merged = df1_dropped.append(df2_dropped)

#clean lists
p2018 = df_merged[df_merged['Anno']==2018.0]
p2019 = df_merged[df_merged['Anno']==2019.0]
p2020 = df_merged[df_merged['Anno']==2020.0] 
p2018_cleaned = clean(list(p2018['Libreria']))
p2019_cleaned = clean(list(p2019['Libreria']))
p2020_cleaned = clean(list(p2020['Libreria']))
total2018 = len(p2018_cleaned)
total2019 = len(p2019_cleaned)
total2020 = len(p2020_cleaned)

#count occurrences of libraries for each year
dict2018 = dict_lib(p2018_cleaned)
dict2019 = dict_lib(p2019_cleaned)
dict2020 = dict_lib(p2020_cleaned)

#group less important libraries in "altro"
dict2018grouped = group(dict2018)
dict2019grouped = group(dict2019)
dict2020grouped = group(dict2020)


#add data manually
years = np.array([2018,2019,2020])
data = pd.DataFrame({
    "SEAL":[13,14,17],
    "HElib":[11,20,11],
    "HEAAN":[5,6,7],
    "TFHE":[3,7,8],
    "Python-Paillier":[3,2,5],
    "PALISADE":[0,3,2],
    "NFLlib":[2,2,0],
    "Custom":[4,3,2],
    "Altro":[1,5,4]
    }, 
    index=years
)

values = np.array([13,11,5,3,3,0,2,4,1,14,20,6,7,2,3,2,3,5,17,11,7,8,5,2,0,2,4])

hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))
r1 = [x * (barWidth / 9) for x in r1]

#plot
data.plot(kind="bar", width=barWidth)
# plt.title("Librerie utilizzate negli anni", fontsize=textsize + 3)
plt.xticks(rotation='horizontal', fontsize=textsize)
plt.yticks(np.arange(0,30,5), fontsize=textsize)
plt.axis(ymin=0, ymax=25)

#insert total and ratio 
padding = 0
for i,v in enumerate(values):
    if i in [0] :
        plt.text(r1[i] + padding - 0.37,v + 0.2 , "{}".format(str(v)), size = textsize)
    elif v < 10 :
        plt.text(r1[i]+ padding - 0.355,v + 0.2 , "{}".format(str(v)), size = textsize)
    elif i % 9 == 0 :
        padding += 0.25
        plt.text(r1[i] + padding - 0.37,v + 0.2 , "{}".format(str(v)), size = textsize)
    else :   
        plt.text(r1[i]+ padding - 0.37,v + 0.2 , "{}".format(str(v)), size = textsize)


#legend
plt.xlabel("Anno")
plt.ylabel("Numero di utilizzi")
plt.legend(loc="best", fontsize=textsize)

plt.tight_layout()

#save figure
plt.savefig('../data/figures/libraries_vs_years.pdf')