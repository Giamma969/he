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

#group less important libraries in 'others' 
def group(d1) :
    l = list()
    for k,v in d1.items() :
        if k in ['Cingulata','Gazelle','GMP', 'ABY','FHEW','PySEAL'] :
            for i in range(v) :
                l.append('Other')
        else :
            for i in range (v) :
                l.append(k)
    #new dictionary with "other" added
    d2 = dict()
    for lib in l :
        d2[lib] = d2.get(lib, 0) + 1
    return d2


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

#group less important libraries in other
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
    "Other":[1,5,4]
    }, 
    index=years
)

# values = np.array([a2018, i2018, m2018, a2019, i2019, m2019, a2020, i2020, m2020])

# hunds = [100 for x in values]
# # Set position of bar on y axis
# r1 = np.arange(len(hunds))
# r1 = [x * 0.165 for x in r1]
# r2 = [x + barWidth for x in r1]

#plot
data.plot(kind="bar", width=0.8)
plt.title("Librerie utilizzate negli anni")
plt.gcf().subplots_adjust(bottom=0.15)
plt.xticks(rotation='horizontal')
plt.yticks(np.arange(0,25,5))
plt.axis(ymin=0, ymax=25)
# plt.tight_layout()

#legend
plt.xlabel("Anno")
plt.ylabel("Numero di utilizzi")


#save figure
plt.savefig('../data/figures/libraries_vs_years.pdf')