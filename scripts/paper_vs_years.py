import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#calculate type of paper for year
def venue_in_year(venue, year) :
    df1 = df_merged[df_merged['Anno'] == year]
    df2 = df1[df1['Tipo Venue'] == venue]
    return (0 if df2.empty else len(df2.index))


#set text size
textsize = 10

#set bar width
barWidth = 0.7

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the columns "Tipo Venue", "Anno", "Libreria" e "Linguaggio"
df1_dropped = df1[['Tipo Venue','Anno']]
df2_dropped = df2[['Tipo Venue','Anno']]

#merge dataframe
df_merged = df1_dropped.append(df2_dropped)

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

values = np.array([j2018, c2018, w2018, j2019, c2019, w2019, j2020, c2020, w2020])

hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))
r1 = [x * 0.165 for x in r1]
r2 = [x + barWidth for x in r1]


plotdata.plot(kind="bar")
plt.title("Papers vs Years")
plt.gcf().subplots_adjust(bottom=0.15)
plt.xticks(rotation='horizontal')
plt.yticks(np.arange(0,50,5))
plt.axis(ymin=0, ymax=50)
# plt.tight_layout()


#insert total and ratio 
increment = 0
for i,v in enumerate(values):
    if i in [3,6] :
        increment += 0.507
    if i in [2,5,8] :
        plt.text(r2[i] + increment - 0.89,v + 0.5 , "{}".format(str(v)), size = textsize)
    else :   
        plt.text(r2[i] + increment - 0.905,v + 0.5 , "{}".format(str(v)), size = textsize)   


#legend
plt.xlabel("Years")
plt.ylabel("Papers")
plt.legend(loc="upper left")

#save figure
plt.savefig('../data/figures/papers_vs_years.pdf', format='pdf')