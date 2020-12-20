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
barWidth = 0.5

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the columns "Tipo Venue","Anno" and merge
df1_dropped = df1[['Tipo Venue','Anno']]
df2_dropped = df2[['Tipo Venue','Anno']]
df_merged = df1_dropped.append(df2_dropped)

years = np.array(df_merged['Anno'])

#nan values are "Fine anno rows"
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


data = pd.DataFrame({
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
r1 = [x * (barWidth/3) for x in r1]


data.plot(kind="bar", width=barWidth, alpha=0.9)
# plt.title("Pubblicazioni negli anni")
plt.xticks(rotation='horizontal')
plt.yticks(np.arange(0,55,5))
plt.axis(ymin=0, ymax=50)

#legend
plt.xlabel("Anno")
plt.ylabel("Numero di pubblicazioni")
plt.legend(loc="upper left")


#insert total and ratio 
padding = 0
for i,v in enumerate(values):
    if i in [0] :
        plt.text(r1[i] + padding - 0.22,v + 0.5 , "{}".format(str(v)), size = textsize)
    elif i in [3,6] :
        padding += barWidth
        plt.text(r1[i] + padding - 0.22,v + 0.5 , "{}".format(str(v)), size = textsize)
    elif i % 3 == 2 :
        plt.text(r1[i] + padding -0.20,v + 0.5 , "{}".format(str(v)), size = textsize)
    else :   
        plt.text(r1[i]+ padding - 0.22,v + 0.5 , "{}".format(str(v)), size = textsize)

plt.tight_layout()

#save figure
plt.savefig('../data/figures/venue_vs_years.pdf', format='pdf')