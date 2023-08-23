#!/usr/bin/env python
# coding: utf-8

# In[33]:


import pandas as pd

satış_datası = pd.read_excel("Satış Datası.xlsx")
print(satış_datası)


#########Toplam satış tutarı###############################
toplam_fiyat = 0
urun_tutarları = satış_datası["URUN_TUTARI"]
urun_adetleri = satış_datası["URUN_ADEDI"]
for i in range(0, len(urun_adetleri)):
    toplam_fiyat += urun_tutarları[i] * urun_adetleri[i]
    
print("Toplam satış tutarı: "+str(toplam_fiyat))
print((urun_tutarları*urun_adetleri).sum())
#########Toplam satış tutarı###############################


#########Toplam fiş sayısı ve ürün adedi##################################
fişler = satış_datası["FIS_ID"]
print()
value_counts = fişler.value_counts()
print(value_counts)

toplam_fiş_sayısı = 0
toplam_urun_adedi = 0
for count in value_counts:
    toplam_fiş_sayısı += count
    
for adet in urun_adetleri:
    toplam_urun_adedi += adet

print("Toplam fiş sayısı:", toplam_fiş_sayısı)
print("Toplam ürün adedi:", toplam_urun_adedi)
#########Toplam fiş sayısı ve ürün adedi##################################


# b. Gün bazında toplam fiş sayısı, toplam satış tutarı ve ortalama sepet tutarı
satış_datası['ALISVERIS_TARIHI'] = pd.to_datetime(satış_datası['ALISVERIS_TARIHI'], format='%Y%m%d')
gunlere_gore_satis = satış_datası.groupby('ALISVERIS_TARIHI').agg(
    ToplamFisSayisi=('FIS_ID', 'nunique'),
    ToplamSatisTutari=('URUN_TUTARI', lambda x: (x * satış_datası.loc[x.index, 'URUN_ADEDI']).sum())
) 
gunlere_gore_satis["OrtalamaSepetTutarı"] = gunlere_gore_satis["ToplamSatisTutari"] / gunlere_gore_satis["ToplamFisSayisi"]

print(gunlere_gore_satis)
    
    
formatlara_gore_fis_tutarlari = satış_datası.groupby('MAGAZA_FORMAT_KODU').apply(lambda group: (group['URUN_TUTARI'] * group['URUN_ADEDI']).describe())
print(formatlara_gore_fis_tutarlari)


print(formatlara_gore_fis_tutarlari[['min', 'mean', '50%', 'max']])
print(formatlara_gore_fis_tutarlari.describe()) ######for statistically describing the data of invoices.
    


# In[22]:


import pandas as pd

urun_kategori_verisi = pd.read_excel("UrunKategori.xlsx")
print(urun_kategori_verisi)


# In[32]:

joined_data = urun_kategori_verisi.merge(satış_datası, on='URUN_KODU')


reyon_bazinda_analiz = joined_data.groupby('REYON_ADI').agg(
    ToplamFisSayisi=('FIS_ID', 'nunique'),
    ToplamHarcamaTutari=('URUN_TUTARI', lambda x: (x * joined_data.loc[x.index, 'URUN_ADEDI']).sum())
)

print(reyon_bazinda_analiz)
print()
print()

en_yuksek_ciro_reyon = reyon_bazinda_analiz['ToplamHarcamaTutari'].idxmax()
print("En yüksek ciro reyon "+str(en_yuksek_ciro_reyon))


highest_ciro_reyon_data = joined_data[joined_data['REYON_ADI'] == en_yuksek_ciro_reyon]


aile_grubu_bazinda_analiz = highest_ciro_reyon_data.groupby('AILE_ADI').agg(
    ToplamFisSayisi=('FIS_ID', 'nunique'),
    ToplamHarcamaTutari=('URUN_TUTARI', lambda x: (x * highest_ciro_reyon_data.loc[x.index, 'URUN_ADEDI']).sum())
)
print()
print()
print(aile_grubu_bazinda_analiz)



en_yuksek_ciro_aile = aile_grubu_bazinda_analiz['ToplamHarcamaTutari'].idxmax()


highest_ciro_aile_data = highest_ciro_reyon_data[highest_ciro_reyon_data['AILE_ADI'] == en_yuksek_ciro_aile]


total_aile_ciro = (highest_ciro_aile_data['URUN_TUTARI'] * highest_ciro_aile_data['URUN_ADEDI']).sum()


ciro_penetrasyonu = highest_ciro_aile_data.groupby('URUN_ISMI').apply(
    lambda group: (group['URUN_TUTARI'] * group['URUN_ADEDI']).sum() / total_aile_ciro
)


total_aile_receipts = highest_ciro_aile_data['FIS_ID'].nunique()


product_receipt_counts = highest_ciro_aile_data.groupby('URUN_ISMI')['FIS_ID'].nunique()

basket_penetrasyonu = product_receipt_counts / total_aile_receipts


print()
print()

print(ciro_penetrasyonu)

print()
print()

print(basket_penetrasyonu)




# In[ ]:




