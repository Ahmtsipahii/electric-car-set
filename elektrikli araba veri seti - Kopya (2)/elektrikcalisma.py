import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("Electric_Vehicle_Population_Data.csv")

# ilk durumda sütun adları ve tablonun durumu 
sutun_adlari = df.columns
print("Sütun Adları:", sutun_adlari)
print(df)


# şehir kullanım sıklığı
#***********************************************************
sehir_kullanim_sikligi = df['City'].value_counts()
print(sehir_kullanim_sikligi)

# En çok kullanılan 15 şehiri seçin
en_cok_kullanilan_15_sehir = sehir_kullanim_sikligi.head(15)

# Grafikleme için seaborn kütüphanesini kullanın
plt.figure(figsize=(12, 6))
sns.barplot(x=en_cok_kullanilan_15_sehir.index, y=en_cok_kullanilan_15_sehir.values, palette="viridis")
plt.title('En Çok Kullanılan 15 Şehirdeki Elektrikli Araba Kullanım Sıklığı', fontsize=16)
plt.xlabel('Şehir', fontsize=14)
plt.ylabel('Kullanım Sıklığı', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.tight_layout()
plt.show()
#****************************************************************



# en uzun menzilli modelleri sıralar
en_uzun_menzil_modeller = df.sort_values(by='Electric Range', ascending=False)['Model'].unique()[:15]
print(en_uzun_menzil_modeller)

# en uzun menzilli 15 aracı grafikle gösterir 
menzil_verisi = df[['Model', 'Electric Range']]

en_uzun_menziller = menzil_verisi.groupby('Model')['Electric Range'].max().reset_index()

en_uzun_menzil_modelleri = en_uzun_menziller.sort_values(by='Electric Range', ascending=False).head(15)

plt.figure(figsize=(12, 8))
sns.barplot(x='Electric Range', y='Model', data=en_uzun_menzil_modelleri, palette='viridis')
plt.title('En Uzun Menzilli 15 Araç Modeli')
plt.xlabel('Menzil (km)')
plt.ylabel('Araç Modeli')
plt.show()


en_cok_bulunan_model = df.groupby(['Make', 'Model']).size().idxmax()

print("En çok bulunan araba markası:", en_cok_bulunan_model[0])
print("En çok bulunan model:", en_cok_bulunan_model[1])


#gereksiz kolonları sildik
df.drop(['State', 'Postal Code','Clean Alternative Fuel Vehicle (CAFV) Eligibility','Base MSRP',
         'Legislative District', 'DOL Vehicle ID',
       'Vehicle Location', 'Electric Utility', '2020 Census Tract',"County","VIN (1-10)"], axis=1, inplace=True)



# menziline göre kullanım amacı adında yeni bir kolon açtık
df['Kullanım Amacı'] = ['Uzun Yol' if x > 300 else 'Şehir İçi' for x in df['Electric Range']]


# tahmini şarj süresi hesapladık ve yeni bir kolon daha açtık
df['şarj süresi'] = df['Electric Range'] / 60  

df['şarj süresi'] = df['şarj süresi'].apply(
    lambda x: " Bilinmiyor" if x == 0 else f"{int(x)} saat" if x >= 1 else f"{int(x * 60)} dakika")


# araç yaşını hesapladık ve yeni bir kolon daha açtık
df['araç yaşı'] = 2025 - df['Model Year']

# bu hesaba göre aracın genel durumunu tahmin ettik
df['aracın model durumu'] = ''

for index, row in df.iterrows():
    if row['araç yaşı'] <= 5:
        df.at[index, 'aracın model durumu'] = 'yüksel modelli'
    elif 5 < row['araç yaşı'] <= 10:
        df.at[index, 'aracın model durumu'] = 'Orta Halli'
    else:
        df.at[index, 'aracın model durumu'] = 'yıpranmış'



# en çok bulunan araba markası modeli ve grafiği 
#*******************************************************************************************
en_cok_bulunan = df.groupby(['Make', 'Model']).size().nlargest(13).reset_index(name='Count')

# Seaborn kütüphanesi ile bar plot çizin
plt.figure(figsize=(12, 8))
sns.barplot(x='Count', y='Model', hue='Make', data=en_cok_bulunan)
plt.title('En Çok Bulunan 15 Araba Markası ve Modelleri')
plt.xlabel('Toplam Sayı')
plt.ylabel('Marka')
plt.show()

en_cok_bulunan_model = df.groupby(['Make', 'Model']).size().idxmax()

#***************************************************


# en çok kullanılan tesla modeli
#*********************************

tesla_models = df[df['Make'] == 'TESLA']['Model'].unique()

# Sonuçları yazdırma
print("Tesla'nın Modelleri:")
print(tesla_models)

tesla_models = df[df['Make'] == 'TESLA']['Model'].value_counts()

# Pasta grafiği oluşturma
plt.figure(figsize=(8, 8))
plt.pie(tesla_models, labels=tesla_models.index, autopct='%1.1f%%', startangle=140)
plt.title("En Çok Kullanılan Tesla Modeller")
plt.show()
#**************************************






# menzil ortalama ve yıllara göre menzil artışı
#********************************************************

ortalama_menzil = df.groupby('Model Year')['Electric Range'].mean().reset_index()


yilyeni = {2011:230,2012:235,2013:250,2014:250,2015:270,2016:330,
       2017:300,2018:350,2019:380,2020:410,2021:440,2022:563,2023:600,2024:850}


for yil, yeni_menzil_degeri in yilyeni.items():
    df.loc[df['Model Year'] == yil, 'Electric Range'] = yeni_menzil_degeri


ortalama_menzil = df.groupby('Model Year')['Electric Range'].mean().reset_index()


# grafik kısmı
plt.figure(figsize=(10, 6))
sns.lineplot(x='Model Year', y='Electric Range', data=ortalama_menzil, marker='o', color='blue')
plt.title('Model Yılına Göre Elektrik Menzil Ortalaması', fontsize=16)
plt.xlabel('Model Yılı', fontsize=14)
plt.ylabel('Elektrik Menzili (km)', fontsize=14)
plt.grid(axis='both', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

#*****************************************************************************


# kullanım amacı 
#********************************************************************
df['Kullanım Amacı'] = ['Uzun Yol' if x > 300 else 'Şehir İçi' for x in df['Electric Range']]

# Genel kullanım amacını gösteren pasta grafiği oluşturma
usage_counts = df['Kullanım Amacı'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(usage_counts, labels=usage_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Elektrikli Araba Kullanım Amacı")
plt.show()


# yıllara göre yakıt tipi dağılımı 
#***********************************************

df_grouped = df.groupby(['Model Year', 'Electric Vehicle Type']).size().unstack()


df_grouped.plot(kind='bar', stacked=True, figsize=(12, 7))


plt.title('Yıllara Göre Yakıt Tipi Dağılımı', fontsize=16)
plt.xlabel('Model Yılı', fontsize=14)
plt.ylabel('Araç Sayısı', fontsize=14)


plt.show()

#********************************************************

print(df)