import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator

#separate multivalued elements and remove inconsistent elements
def clean(types) :
    types_cleaned = list()
    for t in types :
        #separate multivalued elements
        if (type(t) != float and t.find(',') >= 0) :
            t_temp=t.split(', ')
            for elem in t_temp :
                types_cleaned.append(elem)
        #otherwise add if not consistent
        elif (type(t) != float):
            types_cleaned.append(t)
    return types_cleaned

#retrieve a dictionary for HE types
def dict_t(types) :
    d = dict()
    for t in types :
        d[t] = d.get(t, 0) + 1
    return d

#group less important HE types in 'altro' 
def group(d1) :
    l = list()
    for k,v in d1.items() :
        if k in ['PAHE','MK-HE','LinHAE'] :
            for i in range(v) :
                l.append('Altro')
        else :
            for i in range (v) :
                l.append(k)
    #new dictionary with "altro" added
    d2 = dict()
    for t in l :
        d2[t] = d2.get(t, 0) + 1
    return d2



#set text size
textsize = 7

#set bar width
barWidth = 0.75

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the columns "Tipo HE","Anno" and merge
df1_dropped = df1[['Tipo HE','Anno']]
df2_dropped = df2[['Tipo HE','Anno']]
df_merged = df1_dropped.append(df2_dropped)

#clean lists
p2018 = df_merged[df_merged['Anno']==2018.0]
p2019 = df_merged[df_merged['Anno']==2019.0]
p2020 = df_merged[df_merged['Anno']==2020.0] 
p2018_cleaned = clean(list(p2018['Tipo HE']))
p2019_cleaned = clean(list(p2019['Tipo HE']))
p2020_cleaned = clean(list(p2020['Tipo HE']))
total2018 = len(p2018_cleaned)
total2019 = len(p2019_cleaned)
total2020 = len(p2020_cleaned)

#count occurrences of types HE for each year
dict2018 = dict_t(p2018_cleaned)
dict2019 = dict_t(p2019_cleaned)
dict2020 = dict_t(p2020_cleaned)

#group less important types in "altro"
dict2018grouped = group(dict2018)
dict2019grouped = group(dict2019)
dict2020grouped = group(dict2020)

# print('2018', dict2018grouped, '\n')
# print('2019', dict2019grouped, '\n')
# print('2020', dict2020grouped, '\n')

#add data manually
years = np.array([2018,2019,2020])
data = pd.DataFrame({
    "FHE":[18,28,27],
    "HE":[11,18,16],
    "PHE":[8,10,20],
    "LFHE":[5,7,4],
    "SWHE":[6,5,3],
    "APX-HE":[1,1,0],
    "Altro":[2,1,3]
    }, 
    index=years
)

values = np.array([18,11,8,5,6,1,2,28,18,10,7,5,1,1,27,16,20,4,3,0,3])

hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))
r1 = [x * (barWidth / 7) for x in r1]

#plot
data.plot(kind="bar", width=barWidth)
plt.xticks(rotation='horizontal', fontsize=textsize)
plt.yticks(np.arange(0,35,5), fontsize=textsize)
plt.axis(ymin=0, ymax=30)

#insert total and ratio 
padding = 0
for i,v in enumerate(values):
    if i in [0] :
        plt.text(r1[i] + padding - 0.36,v + 0.2 , "{}".format(str(v)), size = textsize)
    elif v < 10 :
        plt.text(r1[i]+ padding - 0.34,v + 0.2 , "{}".format(str(v)), size = textsize)
    elif i % 7 == 0 :
        padding += 0.25
        plt.text(r1[i] + padding - 0.36,v + 0.2 , "{}".format(str(v)), size = textsize)
    else :   
        plt.text(r1[i]+ padding - 0.36,v + 0.2 , "{}".format(str(v)), size = textsize)


#legend
plt.xlabel("Anno")
plt.ylabel("Numero di utilizzi")
plt.legend(loc="best", fontsize=textsize)

plt.tight_layout()

#save figure
plt.savefig('../data/figures/typesHE_vs_years.pdf')