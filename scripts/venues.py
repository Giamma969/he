import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#set text size
textsize = 10

#set bar width
barWidth = 0.9

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Selezione rivisto')
df2 = pd.read_excel (IN_FILE, sheet_name='Snowballing rivisto')

#Extract the column "Tipo Venue" and merge
df1_dropped = df1[['Tipo Venue']]
df2_dropped = df2[['Tipo Venue']]
df_merged = df1_dropped.append(df2_dropped)

#calculate total for each category
Jtot=(len(df_merged[df_merged['Tipo Venue'] == "J"].index))
Ctot=(len(df_merged[df_merged['Tipo Venue'] == "C"].index))
Wtot=(len(df_merged[df_merged['Tipo Venue'] == "W"].index))

names = ["Journal", "Conference", "Workshop"]
values = [Jtot, Ctot, Wtot]

for i, (k,v) in enumerate(zip(names,values)) :
    plt.bar(x=k, width=barWidth, height=v,label=k, alpha=0.8)

hunds = [100 for x in values]
# Set position of bar on y axis
r1 = np.arange(len(hunds))

# Add text on bars
for i,v in enumerate(values):
    if i in [0] :
        plt.text(r1[i] - 0.05, v + 0.7, "{}".format(str(v)), size = textsize)
    else :
        plt.text(r1[i] - 0.05, v + 0.7, "{}".format(str(v)), size = textsize)

# plt.title("Pubblicazioni per tipologia", fontsize=textsize + 2)
# plt.xlim(2,105)
plt.axis(ymax=100)
plt.xticks(fontsize=textsize - 1)
plt.yticks(fontsize=textsize - 1)
plt.xlabel("Tipologia", fontsize=textsize + 1)
plt.ylabel("Numero di pubblicazioni", fontsize=textsize + 1)
plt.legend(loc="upper right")
plt.tight_layout()

#save figure
plt.savefig('../data/figures/venues.pdf', format='pdf')
