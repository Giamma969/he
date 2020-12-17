import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator

#separate multivalued elements and remove inconsistent elements
def clean(languages) :
    languages_cleaned = list()
    for lan in languages :
        #separate multivalued elements
        if (type(lan) != float and lan.find(',') >= 0) :
            lan_temp=lan.split(', ')
            for elem in lan_temp :
                languages_cleaned.append(elem)
        #otherwise add if not consistent
        elif (type(lan) != float):
            languages_cleaned.append(lan)
    return languages_cleaned

#retrieve a dictionary for languages
def dict_lan(languages) :
    d = dict()
    for lan in languages :
        d[lan] = d.get(lan, 0) + 1
    return d


#set text size
textsize = 7

#set bar width
barWidth = 0.75

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the columns "Linguaggio","Anno" and merge
df1_dropped = df1[['Linguaggio','Anno']]
df2_dropped = df2[['Linguaggio','Anno']]
df_merged = df1_dropped.append(df2_dropped)


#clean lists
p2018 = df_merged[df_merged['Anno']==2018.0]
p2019 = df_merged[df_merged['Anno']==2019.0]
p2020 = df_merged[df_merged['Anno']==2020.0] 
p2018_cleaned = clean(list(p2018['Linguaggio']))
p2019_cleaned = clean(list(p2019['Linguaggio']))
p2020_cleaned = clean(list(p2020['Linguaggio']))
total2018 = len(p2018_cleaned)
total2019 = len(p2019_cleaned)
total2020 = len(p2020_cleaned)

#count occurrences of libraries for each year
dict2018 = dict_lan(p2018_cleaned)
dict2019 = dict_lan(p2019_cleaned)
dict2020 = dict_lan(p2020_cleaned)

print(2018,dict2018)
print(2019,dict2019)
print(2020,dict2020)

#add data manually
years = np.array([2018,2019,2020])
data = pd.DataFrame({
    "C++":[14,19,22],
    "Python":[3,9,13],
    "Java":[1,1,2],
    "C#":[1,0,1],
    "C":[0,1,1],
    "GO":[0,0,1]
    }, 
    index=years
)

values = np.array([14,3,1,1,0,0,19,9,1,0,1,0,22,13,2,1,1,1])

hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))
r1 = [x * (barWidth / 6) for x in r1]

#plot
data.plot(kind="bar", width=barWidth)
plt.title("Linguaggi utilizzate negli anni", fontsize=textsize + 3)
plt.xticks(rotation='horizontal', fontsize=textsize)
plt.yticks(np.arange(0,30,5), fontsize=textsize)
plt.axis(ymin=0, ymax=30)

#insert total and ratio 
padding = 0
for i,v in enumerate(values):
    if i in [0] :
        plt.text(r1[i] + padding - 0.35,v + 0.2 , "{}".format(str(v)), size = textsize)
    elif v < 10 :
        plt.text(r1[i]+ padding - 0.335,v + 0.2 , "{}".format(str(v)), size = textsize)
    elif i % 6 == 0 :
        padding += 0.25
        plt.text(r1[i] + padding - 0.35,v + 0.2 , "{}".format(str(v)), size = textsize)
    else :   
        plt.text(r1[i]+ padding - 0.35,v + 0.2 , "{}".format(str(v)), size = textsize)


#legend
plt.xlabel("Anno")
plt.ylabel("Numero di utilizzi")
plt.legend(loc="best", fontsize=textsize)

plt.tight_layout()

#save figure
plt.savefig('../data/figures/languages_vs_years.pdf')