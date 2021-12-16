#Nama : Bilal Fauzan
#NIM : 12220023

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
from PIL import Image
import json

################Membuka file csv dan json###########
file_json = open("kode_negara_lengkap.json")
data = json.loads(file_json.read())

df = pd.read_csv('produksi_minyak_mentah.csv')
df['produksi'] = pd.to_numeric(df['produksi'])
######################################################

##membuat dataframe baru yang mempunyai nama negara, region, dan sub region##
nama_negara=[]
region=[]
sub_region=[]
for i in range (len(df.index)):
    y=0
    indikator = 0
    for k in data:
        if df['kode_negara'][i] == data[y]['alpha-3'] :
            nama_negara.append(data[y]['name'])
            region.append(data[y]['region'])
            sub_region.append(data[y]['sub-region'])
            indikator +=1
        y+=1
    if indikator == 0:
        nama_negara.append(0)
        region.append(0)
        sub_region.append(0)

df['nama_negara']=nama_negara
df['region']=region
df['sub_region']=sub_region
df = df[df.nama_negara != 0]
##################################################################

############### title ###############
st.set_page_config(
    page_title="Visualisasi Data Produksi Minyak Mentah",
    page_icon="logo.png",
    layout="wide",
    menu_items={
         'About': "Nama : Bilal Fauzan \n NIM : 12220023"
    }
    )  # this needs to be the first Streamlit command called
colT1,colT2 = st.columns([3,8])
with colT2:
    st.title("Statistik Produksi Minyak Mentah")
st.markdown("*Sumber data berasal dari soal UAS IF2112 2021*")
#########################################

############### sidebar ###############
image = Image.open('oil_logo.png')
image2 = Image.open('self.jpg')
st.sidebar.title("Argon Oil Company")
st.sidebar.image(image)
st.sidebar.title("Bilal Fauzan (12220023)")
st.sidebar.image(image2)
########################################

############### background image ###############
import base64

main_bg = "sample.jpg"
main_bg_ext = "jpg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)
####################################################

##### User inputs on the control panel #####
st.sidebar.header("Pengaturan konfigurasi tampilan")
nama_negara2=list(dict.fromkeys(nama_negara))
nama_negara2.remove(0)
nama_negara2.sort()
negara = st.sidebar.selectbox("Pilih Negara", nama_negara2)
n_negara = st.sidebar.number_input("Jumlah Negara", min_value=1, max_value=None, value=5)
tahun_unik = list(df['tahun'].unique())
tahun = st.sidebar.selectbox ("Pilih Tahun", tahun_unik)
#################################################

############## Menampilkan Data Keseluruhan #############
colT11,colT12 = st.columns([3,8])
with colT12:
    st.title("Data Produksi Minyak Mentah")
st.dataframe(df)
##########################################################

################## SOAL BAGIAN A ###################
col1, col2 = st.columns([3,1])
col1.subheader("Produksi Minyak Mentah Per Negara")

#membuat list baru jumlah produksi tiap tahun dari negara tersebut
jumlah_prod=[]
for i in df[df['nama_negara']==negara]['produksi'] :
    jumlah_prod.append(i)

#membuat plot
fig, ax = plt.subplots()
cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(tahun_unik)]
ax.bar(tahun_unik, jumlah_prod, color=colors)
ax.set_title(f"Produksi Minyak Mentah {negara}")
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Total Produksi", fontsize=12)
ax.grid(axis='y')
ax.set_axisbelow(True)

col1.pyplot(fig)

#menampilkan data dari plot
col2.subheader("Data")
df_view1 = pd.DataFrame(
    {'Tahun': tahun_unik,
     'Produksi': jumlah_prod
     })
col2.dataframe(df_view1, 300, 475)
####################################################

################## SOAL BAGIAN B ###################
col3, col4 = st.columns([3,1])
col3.subheader("Produksi Minyak Mentah Terbesar")

#mengurutkan dataframe dan memasukannya ke dalam list baru untuk dibuat plot
df_2 = df.sort_values(by=['produksi'], ascending=False)
df_2 = df_2.loc[df_2['tahun']==tahun]
jumlah_produksi = []
list_negara=[]
x=0
for i in df_2['produksi']:
    if x < n_negara:
        jumlah_produksi.append(i)
        x+=1
x=0
for i in df_2['nama_negara']:
    if x < n_negara:
        list_negara.append(i)
        x+=1

#membuat plot
fig, ax = plt.subplots()
ax.barh(list_negara, jumlah_produksi, color=colors)
ax.set_title(f"Produksi Minyak Mentah Terbesar {n_negara} Negara Pada Tahun {tahun}")
ax.set_yticklabels(list_negara, rotation=0)
ax.invert_yaxis()
ax.set_xlabel("Total Produksi", fontsize=12)
ax.grid(axis='x')
ax.set_axisbelow(True)

plt.tight_layout()

col3.pyplot(fig)

#menampilkan data dari plot
col4.subheader("Data")
df_view2 = pd.DataFrame(
    {'Negara': list_negara,
     'Produksi': jumlah_produksi
     })
col4.dataframe(df_view2, 300, 475)
####################################################

################## SOAL BAGIAN C ###################
col5, col6 = st.columns([3,1])
col5.subheader("Produksi Minyak Mentah Terbesar Secara Kumulatif")

#membuat dataframe baru dan membuat kolom baru total produksi dan memasukan ke dalam list untuk dibuat plot
df_3 = pd.DataFrame(df, columns= ['nama_negara','produksi'])
df_3['total_prod'] =  df_3.groupby(['nama_negara'])['produksi'].transform('sum')
del df_3['produksi']
df_3 = df_3.drop_duplicates(subset=['nama_negara'])
df_3=df_3.sort_values(by=['total_prod'], ascending=False)
list_negara2=[]
total_prod=[]
y=0
for i in df_3['total_prod']:
    if y < n_negara:
        total_prod.append(i)
        y+=1
y=0
for i in df_3['nama_negara']:
    if y < n_negara:
        list_negara2.append(i)
        y+=1

#membuat plot
fig, ax = plt.subplots()
ax.barh(list_negara2, total_prod, color=colors)
ax.set_title(f"Produksi Kumulatif Minyak Mentah Terbesar {n_negara} Negara")
ax.set_yticklabels(list_negara2, rotation=0)
ax.invert_yaxis()
ax.set_xlabel("Total Produksi", fontsize=12)
ax.grid(axis='x')
ax.set_axisbelow(True)

plt.tight_layout()

col5.pyplot(fig)

#menampilkan data dari plot
col6.subheader("Data")
df_view3 = pd.DataFrame(
    {'Negara': list_negara2,
     'Produksi': total_prod
     })
col6.dataframe(df_view3, 300, 475)
####################################################

################## SOAL BAGIAN D ###################
######## 1 ###########
colT3,colT4 = st.columns([3,8])
with colT4:
    st.header("Produksi Minyak Mentah Terbesar")
col7, col8 = st.columns(2)

#membuat list baru dan memasukkan nilai terbesar pada list tersebut
list_max_all=[]
list_max=[]
df_4_1 = df.sort_values(by=['produksi'], ascending=False)
for i in df_4_1.iloc[0,:]:
    list_max_all.append(i)
df_4_2 = df_4_1.loc[df_4_1['tahun']==tahun]
for i in df_4_2.iloc[0,:]:
    list_max.append(i)
list_negara3=[list_max[3],list_max_all[3]]
list_prod=[list_max[2],list_max_all[2]]

#menampilkan data berupa text
col7.subheader(f"Produksi pada tahun {tahun} :")
col7.markdown(f"{list_max[3]} ({list_max[0]})")
col7.markdown(f"Region : {list_max[4]}, Sub Region : {list_max[5]}")
col7.markdown(f"Jumlah Produksi Minyak Mentah : {list_max[2]}")

col8.subheader(f"Keseluruhan tahun :")
col8.markdown(f"{list_max_all[3]} ({list_max_all[0]})")
col8.markdown(f"Region : {list_max_all[4]}, Sub Region : {list_max_all[5]}")
col8.markdown(f"Jumlah Produksi Minyak Mentah : {list_max_all[2]}")

#menampilkan data berupa plot
colT3,colT4 = st.columns([1,8])
fig, ax = plt.subplots()
ax.barh(list_negara3, list_prod, color=colors)
ax.set_xlabel("Total Produksi", fontsize=12)
ax.grid(axis='x')
ax.set_axisbelow(True)
plt.tight_layout()
colT4.pyplot(fig)
#####################

######## 2 ###########
colT5,colT6 = st.columns([3,8])
with colT6:
    st.header("Produksi Minyak Mentah Terkecil")
col9, col10 = st.columns(2)

#membuat list baru dan memasukkan nilai terkecil pada list tersebut
list_low_all=[]
list_low=[]
mask = df['produksi'] != 0
df_5_1 = df[mask].sort_values(by=['produksi'])
for i in df_5_1.iloc[0,:]:
    list_low_all.append(i)
df_5_2 = df_5_1.loc[df_5_1['tahun']==tahun]
for i in df_5_2.iloc[0,:]:
    list_low.append(i)

list_negara4=[list_low[3],list_low_all[3]]
list_prod2=[list_low[2],list_low_all[2]]

#menampilkan data berupa text
col9.subheader(f"Produksi pada tahun {tahun} :")
col9.markdown(f"{list_low[3]} ({list_low[0]})")
col9.markdown(f"Region : {list_low[4]}, Sub Region : {list_low[5]}")
col9.markdown(f"Jumlah Produksi Minyak Mentah : {list_low[2]}")

col10.subheader(f"Keseluruhan tahun :")
col10.markdown(f"{list_low_all[3]} ({list_low_all[0]})")
col10.markdown(f"Region : {list_low_all[4]}, Sub Region : {list_low_all[5]}")
col10.markdown(f"Jumlah Produksi Minyak Mentah : {list_low_all[2]}")

#menampilkan data berupa plot
colT5,colT6 = st.columns([1,8])
fig, ax = plt.subplots()
ax.barh(list_negara4, list_prod2, color=colors)
ax.set_xlabel("Total Produksi", fontsize=12)
ax.grid(axis='x')
ax.set_axisbelow(True)
plt.tight_layout()
colT6.pyplot(fig)
#####################

######## 3 ###########
colT7,colT8 = st.columns([3,8])
with colT8:
    st.header("Produksi Minyak Mentah Sama Dengan Nol")
col11, col12 = st.columns(2)

#memfilter data dengan value produksi = 0
df_6_1 = df[df.produksi == 0]
df_6_2 = df_6_1.loc[df_6_1['tahun']==tahun]

#menampilkan data dalam bentuk dataframe
col11.subheader(f"Produksi pada tahun {tahun} :")
col11.dataframe(df_6_2)

col12.subheader(f"Keseluruhan tahun :")
col12.dataframe(df_6_1)
###############################################################

### Tambahan
############### rata-rata produksi tiap tahun #################
colT9,colT10 = st.columns([3,8])
with colT10:
    st.header("Rata-Rata Produksi Minyak Mentah Dunia")
col13, col14 = st.columns([3,1])

#Menjumlahkan produksi tiap tahun dan membuat kolom baru total produksinya kemudian menambahkan kedalam list
df_7 = pd.DataFrame(df, columns= ['tahun','produksi'])
df_7['total_prod'] =  df_7.groupby(['tahun'])['produksi'].transform('sum')
df_7 = df_7.drop_duplicates(subset=['tahun'])
del df_7['produksi']
df_7['total_prod'] = df_7['total_prod'].apply(lambda x: x/len(df_3))
prod_rata=[]
for i in df_7['total_prod']:
    prod_rata.append(i)

col13.subheader("Grafik Rata-Rata Produksi Minyak Mentah Dunia Tiap Tahun")

#Menampilkan data berupa plot
fig, ax = plt.subplots()
ax.plot(tahun_unik, prod_rata)
ax.set_title("Rata-Rata Produksi Minyak Mentah Dunia Tiap Tahun")
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Total Produksi", fontsize=12)
ax.grid(axis='both')
ax.set_axisbelow(True)
plt.tight_layout()
col13.pyplot(fig)

col14.subheader("Data")

#Menampilkan data berupa dataframe
df7_view = pd.DataFrame(
    {'Tahun': tahun_unik,
     'Produksi': prod_rata
     })
col14.dataframe(df7_view, 300, 475)
###############################################################

############### Perbandingan Produksi X Negara  #################
st.sidebar.subheader("Perbandingan Produksi")
per_negara = st.sidebar.multiselect("Pilih Negara (untuk memunculkan grafik)", nama_negara2)

colT11,colT12 = st.columns([3,8])
with colT12:
    st.header("Perbandingan Produksi Minyak Mentah Tiap Negara")
st.subheader("Grafik Perbandingan Produksi Minyak Mentah")
df_baru=pd.DataFrame(index =tahun_unik)
penampung_data=[]
for i in per_negara:
    prod_per_negara = []
    for x in df[df['nama_negara']==i]['produksi'] :
        prod_per_negara.append(x)
    df_baru[i]=prod_per_negara

st.line_chart(data=df_baru)