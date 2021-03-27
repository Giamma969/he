import pandas as pd

#possible features
v1='Needs further study to be usable'
v2='It can be used'
v3='It can be used partially'
v1_='Not specified usable'
v4='Need to improve performance'
v5='Needs to improve accuracy'
v6='Need to reduce overhead (computational cost) due from HE'
v7='Need to reduce overhead (storage) due from HE'
v8='Need to improve performance not specified'
v9='--> Implementing HE optimizations'
v10='--> Use bootstrapping'
v11='--> Use SIMD'
v12='--> Vary the setup parameters'
v13='--> Use a different homomorphic schema'
v14='--> Applying parallelism'
v15='--> Externalizing the encryption service using micro services'
v16='--> Use HW solutions'
v17='Needs to improve security'
v18='Need for the number of iterations to be provided in advance'
v19='Difficulty of developing HE-based applications'
v20='--> Apply the proposed solution to concrete use-cases'
v21='--> Test the work on further data'
v22='--> Advancement of HE technologies'
v23='--> Extend the protocol to apply it to different scenarios'
v24='--> Extend the work to other ML algorithms'
v25='--> They will use a non-HE based solution'

IN_FILE = '../data/search_and_snowballing_HE.xlsx'
OUT_FILE = '../data/future_challenges.txt'

#take both original sheets
df1 = pd.read_excel (IN_FILE, sheet_name='Selezione rivisto')
df2 = pd.read_excel (IN_FILE, sheet_name='Snowballing rivisto')

#Extract the column "Tipo HE" and merge
df1_dropped = df1[['Future challenges topics']]
df2_dropped = df2[['Future challenges topics']]
df_merged = df1_dropped.append(df2_dropped)


f = open(OUT_FILE, "w")


#create dictionary and count improve perormance not specified
counts = dict()
blocks = list(df_merged['Future challenges topics'])

for block in blocks :
    found_others = False
    found_perf = False
    if (type(block) != float) :
        topics = block.split('\n')
        for topic in topics :
            counts[topic] = counts.get(topic, 0) + 1
            if (topic==v5 or topic==v6 or topic==v7) :
                found_others = True
            if (topic == v4) :
                found_perf = True
        if(found_perf==True and found_others==False) :
            counts[v8] = counts.get(v8,0) + 1
            

#calculate usable not specified 
usable_NS = 187 - counts.get(v1) - counts.get(v2) - counts.get(v3)

#order dictionary
ordered = list() 

l1=[v1, counts.get(v1)]
l2=[v2, counts.get(v2)]
l3=[v3, counts.get(v3)]
l1_=[v1_, usable_NS]
l4=[v4, counts.get(v4)]
l5=[v5, counts.get(v5)]
l6=[v6, counts.get(v6)]
l7=[v7, counts.get(v7)]
l8=[v8, counts.get(v8)]
l9=[v9, counts.get(v9)]
l10=[v10, counts.get(v10)]
l11=[v11, counts.get(v11)]
l12=[v12, counts.get(v12)]
l13=[v13, counts.get(v13)]
l14=[v14, counts.get(v14)]
l15=[v15, counts.get(v15)]
l16=[v16, counts.get(v16)]
l17=[v17, counts.get(v17)]
l18=[v18, counts.get(v18)]
l19=[v19, counts.get(v19)]
l20=[v20, counts.get(v20)]
l21=[v21, counts.get(v21)]
l22=[v22, counts.get(v22)]
l23=[v23, counts.get(v23)]
l24=[v24, counts.get(v24)]
l25=[v25, counts.get(v25)]


ordered.append(l1)
ordered.append(l2)
ordered.append(l3)
ordered.append(l1_)
ordered.append(l4)
ordered.append(l5)
ordered.append(l6)
ordered.append(l7)
ordered.append(l8)
ordered.append(l9)
ordered.append(l10)
ordered.append(l11)
ordered.append(l12)
ordered.append(l13)
ordered.append(l14)
ordered.append(l15)
ordered.append(l16)
ordered.append(l17)
ordered.append(l18)
ordered.append(l19)
ordered.append(l20)
ordered.append(l21)
ordered.append(l22)
ordered.append(l23)
ordered.append(l24)
ordered.append(l25)


#write values on file
for elem in ordered :
    i=0
    for v in elem :
        if(v==v4 or v==v9 or v==v14 or v==v17) :
            f.write("\n")
        if(v==v5 or v==v6 or v==v7 or v==v8 or v==v24) :
            f.write("\t")
        if(v==v9 or v==v10 or v==v11 or v==v12 or v==v13 or v==v14 or v==v15 or v==v16 ) :
            f.write("\t\t")
            if(v==v9) :
                f.write("HE techniques\n\t\t")
            if(v==v14) :
                f.write("Non-HE techniques\n\t\t")
        f.write(str(v))
        if(i==0):
            f.write(" >>> ")
            i+=1
    f.write("\n")

f.close()

