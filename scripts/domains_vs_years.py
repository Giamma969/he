import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator

#separate multivalued elements and remove inconsistent elements
def clean(domains) :
    domains_cleaned = list()
    for dom in domains :
        #separate multivalued elements
        if (type(dom) != float and dom.find(',') >= 0) :
            dom_temp=dom.split(', ')
            for elem in dom_temp :
                domains_cleaned.append(elem)
        #otherwise add if not consistent
        elif (type(dom) != float):
            domains_cleaned.append(dom)
    return domains_cleaned

#retrieve a dictionary for domains
def dict_dom(domains) :
    d = dict()
    for dom in domains :
        d[dom] = d.get(dom, 0) + 1
    return d

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
df1 = pd.read_excel (IN_FILE, sheet_name='Selezione rivisto')
df2 = pd.read_excel (IN_FILE, sheet_name='Snowballing rivisto')

#Extract the columns "Dominio","Anno" and merge
df1_dropped = df1[['Dominio','Anno']]
df2_dropped = df2[['Dominio','Anno']]
df_merged = df1_dropped.append(df2_dropped)

#clean lists
p2018 = df_merged[df_merged['Anno']==2018.0]
p2019 = df_merged[df_merged['Anno']==2019.0]
p2020 = df_merged[df_merged['Anno']==2020.0] 
p2018_cleaned = clean(list(p2018['Dominio']))
p2019_cleaned = clean(list(p2019['Dominio']))
p2020_cleaned = clean(list(p2020['Dominio']))
total2018 = len(p2018_cleaned)
total2019 = len(p2019_cleaned)
total2020 = len(p2020_cleaned)

#count occurrences of libraries for each year
dict2018 = dict_dom(p2018_cleaned)
dict2019 = dict_dom(p2019_cleaned)
dict2020 = dict_dom(p2020_cleaned)


# print(2018,dict2018,'\n')
# print(2019,dict2019,'\n')
# print(2020,dict2020,'\n')


#insert data manually
domains = ['Machine Learning','Cloud Computing', 'Genomica', 'Riconoscimento Biometrico', 'IoT', 'Medicina','Image Processing', 'Recommender Systems', 'Query Processing','Finanza', 'Sicurezza Informatica', 'Smart City', 'Unmanned Systems', 'Compilatori', 'Database', 'Smart Grid', 'Social Networks', 'Big Data', 'Blockchain', 'Wireless Sensor Networks','Mobile', 'Forensic','Video Compression']


values_2018 = [23,2,5,3,0,1,5,2,3,1,0,1,1,1,0,0,0,1,0,2,0,1,1]
values_2019 = [34,17,2,4,4,4,3,2,1,2,3,3,2,1,1,1,0,0,0,0,1,0,0]
values_2020 = [35,8,8,6,7,5,2,2,1,2,2,0,0,1,2,2,2,1,2,0,1,0,0]
ratios_2018 = calculate_ratios(values_2018,total2018)
ratios_2019 = calculate_ratios(values_2019,total2019)
ratios_2020 = calculate_ratios(values_2020,total2020)
domains.reverse()
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
# plt.title("Domini di applicazione negli anni", fontsize=9)
plt.xlim(0,45)
plt.ylim(-1,len(domains) * 3)
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
plt.ylabel('Domini', fontsize=textsize)
plt.xlabel('Numero di utilizzi (%)', fontsize=textsize)
plt.xticks(np.arange(0,50,5), fontsize=textsize)
plt.yticks([r + barWidth for r in r1], domains, fontsize=textsize)
plt.xticks(fontsize=textsize) 

# Create legend & Show graphic
plt.legend(fontsize=textsize, loc='lower right')
plt.tight_layout()

#save figure
plt.savefig('../data/figures/domains_vs_years.pdf')