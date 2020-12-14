import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#calculate type of paper for year
def venue_in_year(venue, year) :
    df1 = df_merged[ df_merged['Anno'] == year]
    df2 = df1 [df1['Tipo Venue'] == venue] 
    #"df2.index" also counts the nan values --> some value in 'Tipo Venue' column are nan
    return (0 if df2.empty else len(df2.index))


IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the columns "Tipo Venue", "Anno", "Libreria" e "Linguaggio"
df1_dropped = df1[['Tipo Venue','Anno', 'Libreria','Linguaggio']]
df2_dropped = df2[['Tipo Venue','Anno', 'Libreria','Linguaggio']]

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
# plt.grid(True, alpha=0.5)
# plt.show()
plt.savefig('../data/libreries_total.pdf', format='pdf')

#############################################################################
#count type of venue for year



years = np.array(df_merged['Anno'])

#!!! Temporary, some years are nan. Why???
years = years[np.logical_not(np.isnan(years))]


#take unique years
yrs = list()
for y in years :
    y=int(y)
    if y in yrs :
        continue
    yrs.append(y)


#calculate type of paper for year
j2018 = venue_in_year("J", 2018)
c2018 = venue_in_year("C", 2018)
w2018 = venue_in_year("W", 2018)
j2019 = venue_in_year("J", 2019)
c2019 = venue_in_year("C", 2019)
w2019 = venue_in_year("W", 2019)
j2020 = venue_in_year("J", 2020)
c2020 = venue_in_year("C", 2020)
w2020 = venue_in_year("W", 2020)


# fig, ax = plt.subplots()
plotdata = pd.DataFrame({
    "Journal":[j2018, j2019, j2020],
    "Conference":[c2018, c2019, c2020],
    "Workshop":[w2018, w2019, w2020]
    }, 
    index=np.sort(np.array(yrs))
)

plotdata.plot(kind="bar")
plt.xticks(rotation='horizontal')
plt.yticks(np.arange(0,50,5))
plt.title("Papers vs Years")
plt.xlabel("Years")
plt.ylabel("Papers")
plt.legend(loc="upper left")
plt.savefig('../data/papers_vs_years.pdf', format='pdf')

