import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#calculate type of paper for year
def indinv_in_year(indinv, year) :
    df1 = df_merged[df_merged['Anno'] == year]
    df2 = df1[df1['Industry involvement'] == indinv]
    return (0 if df2.empty else len(df2.index))


#set text size
textsize = 10

#set bar width
barWidth = 0.7

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the columns "Industry involvement","Anno" and merge
df1_dropped = df1[['Industry involvement','Anno']]
df2_dropped = df2[['Industry involvement','Anno']]
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


# #calculate type of paper for year
a2018 = indinv_in_year("A", 2018)
i2018 = indinv_in_year("I", 2018)
m2018 = indinv_in_year("M", 2018)
a2019 = indinv_in_year("A", 2019)
i2019 = indinv_in_year("I", 2019)
m2019 = indinv_in_year("M", 2019)
a2020 = indinv_in_year("A", 2020)
i2020 = indinv_in_year("I", 2020)
m2020 = indinv_in_year("M", 2020)


# fig, ax = plt.subplots()
plotdata = pd.DataFrame({
    "Academy":[a2018, a2019, a2020],
    "Industry":[i2018, i2019, i2020],
    "Mix":[m2018, m2019, m2020]
    }, 
    index=np.sort(np.array(yrs))
)

values = np.array([a2018, i2018, m2018, a2019, i2019, m2019, a2020, i2020, m2020])

hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))
r1 = [x * 0.165 for x in r1]
r2 = [x + barWidth for x in r1]


plotdata.plot(kind="bar")
plt.title("Industry involvement vs Years")
plt.gcf().subplots_adjust(bottom=0.15)
plt.xticks(rotation='horizontal')
plt.yticks(np.arange(0,50,5))
plt.axis(ymin=0, ymax=52)
# plt.tight_layout()


#insert total and ratio 
increment = 0
for i,v in enumerate(values):
    if i in [3,6] :
        increment += 0.507
    if i in [1,4,7] :
        plt.text(r2[i] + increment - 0.88,v + 0.5 , "{}".format(str(v)), size = textsize)
    else :   
        plt.text(r2[i] + increment - 0.895,v + 0.5 , "{}".format(str(v)), size = textsize)   


#legend
plt.xlabel("Years")
plt.ylabel("Industry involvement")
plt.legend(loc="upper right")

#save figure
plt.savefig('../data/figures/indinv_vs_years.pdf')