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


#group 'Altro' if type != FHE and type != HE 
def group(types) :
    l = list()
    for elem in types :
        if elem != 'HE' and elem != 'FHE' :
            l.append('Altro')
        else :
            l.append(elem)
    return l


#retrieve a dictionary for HE types
def dict_t(types) :
    d = dict()
    for t in types :
        d[t] = d.get(t, 0) + 1
    return d


#set text size
textsize = 7

#set bar width
barWidth = 0.75

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Selezione rivisto')
df2 = pd.read_excel (IN_FILE, sheet_name='Snowballing rivisto')

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

#group less important types in "altro"
grouped2018 = group(p2018_cleaned)
grouped2019 = group(p2019_cleaned)
grouped2020 = group(p2020_cleaned)

#count occurrences of types HE for each year
dict2018 = dict_t(grouped2018)
dict2019 = dict_t(grouped2019)
dict2020 = dict_t(grouped2020)

print(2018, dict2018)
print(2018, dict2019)
print(2018, dict2020)

#add data manually

years = np.array([2018,2019,2020])
data = pd.DataFrame({
    "FHE":[18,28,27],
    "Altro":[22,24,30],
    "HE":[11,18,16]
    }, 
    index=years
)

values = np.array([18,22,11,28,24,18,27,30,16])


hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))
r1 = [x * (barWidth / 3) for x in r1]

#plot
data.plot(kind="bar", width=barWidth)
plt.xticks(rotation='horizontal', fontsize=textsize)
plt.yticks(np.arange(0,40,5), fontsize=textsize)
plt.axis(ymin=0, ymax=35)

#insert total and ratio 
padding = 0
for i,v in enumerate(values):
    if i in [0] :
        plt.text(r1[i] + padding - 0.29,v + 0.2 , "{}".format(str(v)), size = textsize)
    elif i % 3 == 0 :
        padding += 0.25
        plt.text(r1[i] + padding - 0.29,v + 0.2 , "{}".format(str(v)), size = textsize)
    else :   
        plt.text(r1[i]+ padding - 0.29,v + 0.2 , "{}".format(str(v)), size = textsize)


#legend
plt.xlabel("Anno")
plt.ylabel("Numero di utilizzi")
plt.legend(loc="upper left", fontsize=textsize)

plt.tight_layout()

#save figure
plt.savefig('../data/figures/fhe_vs_other_years.pdf')


