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
barWidth = 0.5

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Selezione rivisto')
df2 = pd.read_excel (IN_FILE, sheet_name='Snowballing rivisto')

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


plotdata = pd.DataFrame({
    "Università":[a2018, a2019, a2020],
    "Industria":[i2018, i2019, i2020],
    "Mix":[m2018, m2019, m2020]
    }, 
    index=np.sort(np.array(yrs))
)

values = np.array([a2018, i2018, m2018, a2019, i2019, m2019, a2020, i2020, m2020])

hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))
r1 = [x * (barWidth/3) for x in r1]


plotdata.plot(kind="bar", width=barWidth, alpha=0.9)
# plt.title("Coinvolgimento delle industrie negli anni")
plt.xticks(rotation='horizontal')
plt.yticks(np.arange(0,55,5))
plt.axis(ymin=0, ymax=52)

#legend
plt.xlabel("Anno")
plt.ylabel("Numero di pubblicazioni")
plt.legend(loc="upper left")

plt.tight_layout()


#insert total and ratio 
padding = 0
for i,v in enumerate(values):
    if i in [3,6] :
        padding += barWidth
        plt.text(r1[i] + padding - 0.22,v + 0.5 , "{}".format(str(v)), size = textsize)
    elif i % 3 == 1 :
        plt.text(r1[i] + padding - 0.2,v + 0.5 , "{}".format(str(v)), size = textsize)
    else :   
        plt.text(r1[i] + padding - 0.22,v + 0.5 , "{}".format(str(v)), size = textsize)


#save figure
plt.savefig('../data/figures/indinv_vs_years.pdf')