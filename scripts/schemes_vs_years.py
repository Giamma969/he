import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator

#separate multivalued elements and remove inconsistent elements
def clean(schemes) :
    schemes_cleaned = list()
    for s in schemes :
        #separate multivalued elements
        if (type(s) != float and s.find(',') >= 0) :
            s_temp=s.split(', ')
            for elem in s_temp :
                schemes_cleaned.append(elem)
        #otherwise add if not consistent
        elif (type(s) != float):
            schemes_cleaned.append(s)
    return schemes_cleaned

#retrieve a dictionary for schemes
def dict_s(schemes) :
    sc = dict()
    for s in schemes :
        sc[s] = sc.get(s, 0) + 1
    return sc

def calculate_ratios(values, tot) :
    ratios = []
    for v in values :
        try:
            ratios.append(round((v * 100) / tot, 2))
        except ZeroDivisionError:
            ratios.append(0)
    return ratios



#set text size
textsize = 8.5

#set bar width
barWidth = 0.8

IN_FILE = '../data/search_and_snowballing_HE.xlsx'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Copia selezione')
df2 = pd.read_excel (IN_FILE, sheet_name='Copia snowballing')

#Extract the columns "Schema di crittografia","Anno" and merge
df1_dropped = df1[['Schema di crittografia','Anno']]
df2_dropped = df2[['Schema di crittografia','Anno']]
df_merged = df1_dropped.append(df2_dropped)

#clean lists
p2018 = df_merged[df_merged['Anno']==2018.0]
p2019 = df_merged[df_merged['Anno']==2019.0]
p2020 = df_merged[df_merged['Anno']==2020.0] 
p2018_cleaned = clean(list(p2018['Schema di crittografia']))
p2019_cleaned = clean(list(p2019['Schema di crittografia']))
p2020_cleaned = clean(list(p2020['Schema di crittografia']))
total2018 = len(p2018_cleaned)
total2019 = len(p2019_cleaned)
total2020 = len(p2020_cleaned)

#count occurrences of schemes for each year
dict2018 = dict_s(p2018_cleaned)
dict2019 = dict_s(p2019_cleaned)
dict2020 = dict_s(p2020_cleaned)


# print(2018,dict2018,'\n')
# print(2019,dict2019,'\n')
# print(2020,dict2020,'\n')

# insert data manually
schemes = ['BFV','CKKS','Paillier','BGV','TFHE','Custom','CKKS-RNS','BGV custom','ElGamal','LNV','BGN','YASHE','BFV custom','MORE','BFV-RNS','DDH','MS-FHE','JL','Paillier custom','SV custom','RSA','CRT','FHEW','CKKS custom','NTRU','MORE custom']




values_2018 = [14,5,8,8,4,4,1,1,0,1,1,2,1,0,2,0,0,0,0,0,0,1,0,0,0,0]
values_2019 = [14,13,7,10,8,5,1,2,0,2,1,0,1,2,0,1,1,1,0,0,0,0,0,0,0,0]

values_2020 = [12,15,15,4,7,5,3,1,3,0,0,0,0,0,0,1,0,0,1,1,1,0,1,1,1,1] 

ratios_2018 = calculate_ratios(values_2018,total2018)
ratios_2019 = calculate_ratios(values_2019,total2019)
ratios_2020 = calculate_ratios(values_2020,total2020)
schemes.reverse()
values_2018.reverse()
values_2019.reverse()
values_2020.reverse()
ratios_2018.reverse()
ratios_2019.reverse()
ratios_2020.reverse()


hunds = [100 for x in values_2018]

# Set position of bar on y axis
r1 = np.arange(len(hunds))
r1 = [3 * x for x in r1]
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]


# Make the plot
fig = plt.figure(num=None, figsize=(6, 11), dpi=80)
plt.xlim(0,25)
plt.ylim(-1,len(schemes) * 3)
plt.barh(r3, values_2018, height=barWidth, label='2018')
plt.barh(r2, values_2019, height=barWidth, label='2019')
plt.barh(r1, values_2020, height=barWidth, label='2020')

# Add text on bars
for i, (v, p) in enumerate(zip(values_2018, ratios_2018)):
    if v not in [0]:
        plt.text(v + 0.4, r1[i] + 1.3, "{} ({}%)".format(str(v),str(p)), size = textsize)
    else:
        plt.text(v + 0.4, r1[i] + 1.3, "-", size = textsize)
    
for i, (v, p) in enumerate(zip(values_2019, ratios_2019)):
    if v not in [0]:
        plt.text(v + 0.4, r2[i] - 0.3 , "{} ({}%)".format(str(v),str(p)), size = textsize)
    else:
        plt.text(v + 0.4, r2[i] - 0.3, "-", size = textsize)

for i, (v, p) in enumerate(zip(values_2020, ratios_2020)):
    if v not in [0]:
        plt.text(v + 0.4, r3[i] - 1.9 , "{} ({}%)".format(str(v),str(p)), size = textsize)
    else:
        plt.text(v + 0.4, r3[i] - 1.9, "-", size = textsize)



# Add xticks on the middle of the group bars
plt.ylabel('Crittosistemi omomorfi', fontsize=textsize)
plt.xlabel('Numero di utilizzi (%)', fontsize=textsize)
plt.xticks(np.arange(0,30,5), fontsize=textsize)
plt.yticks([r + barWidth for r in r1], schemes, fontsize=textsize)
plt.xticks(fontsize=textsize) 

# Create legend & Show graphic
plt.legend(fontsize=textsize, loc='lower right')
plt.tight_layout()

#save figure
plt.savefig('../data/figures/schemes_vs_years.pdf')