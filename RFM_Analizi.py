##############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
# RFM Nedir? Recency, Frequency, Monetary kelimelerinin baş harflerinden meydana gelen bir isimlendirmedir.

# => Kural tabanlı Müşteri segmantasyonu için kullanılan bir tekniktir.

# => Müşterilerin satın alma alışkanlıkları üzerinden grouplara ayrılması ve bu gruplar özelinde stratejiler
# geliştirilebilmesini sağlar.

# => CRM çalışmaları için birçok başlıkta veriye dayalı aksiyon alma imkanı sağlar.

# => Recency, Frequency, Monetary değerleri RFM teknikleridir.


# Recency Değeri (Yenilik): Bizden ( yani herhangi bir işletmeden) en son ne zaman alış veriş yaptığını ifade eder.
# Örneğin bir müşterinin Recency değeri 1, diğer müşterinin Recency değeri 10 ise bizim için 1 olan değere sahip müşteri
# daha iyidir. Çünkü Recency değeri ile iyi olma durumu arasında ters ilişki vardır. Recency değeri ne kadar küçük ise
# bizim için o kadar iyidir. Recency değeri küçük demek o müşteri daha yakın zamanda bizden alışveriş yapmış demek.
# Recency değeri büyük demek o müşteri bizden daha uzak bir tarihte alış veriş yapmış demek.
# Bu değerin matematiksel olarak hesaplanması karşılığı şu şekildedir:
# Analizin yapıldığı tarih  -(eksi) ilgili müşterinin son satın almayı yaptığı tarihtir.

# Frequency Değeri (Sıklık): Örneğin Müşterinin yaptığı toplam alış veriş sayısıdır. Diğer bir ifade ile işlem sayısıdır
# Freqyency değeri ile iyi olma durumu arasında doğru orantılı bir ilişki vardır. Frequency değeri büyüdükçe bizim için
# iyi demektir. Bir müşterinin Frequency değeri 50, diğer bir müşterinin Frequency değeri 30 ise, 50 olan müşteeri bizim
# için daha iyidir.
# Bu değerin matematiksel karşılığı ise:
# Müşterinin yaptığı toplam satınalmadır.

# Monetary (Parasal Değer): Bu değer de bize müşterilerin bize bıraktığı parasal değeri ifade eder. Monetary değeri ile
# iyi olma durumu arasında doğru orantı vardır. Monetary değeri ne kadar büyük ise bizim için işletme için o kadar
# iyidir. Örneğin A müşterisinin Monetary değeri 5000 B müşterisinin Monetary değeri 2000 ise A müşterisi bizim için
# daha önemlidir diyebiliriz.
# Bu değerin matematiksel karşılığı ise:
# Müşterinin yaptığı bu toplam satın almalar neticesinde bıraktığı toplam parasal değerdir.

# Bilgi: Yuıkarıda bahsedilen RFM metrikleri RFM skorlarına çevrilmelidir. Farklı veri tipine sahip bu metrikleri,
# karşılaştırma yapabilmek için aynı veri tipine çevrilmelidir. Yani bunları skorlara çevirmek demek hepsini aynı
# cinsten ifade etmek demektir. Yani bir çeşit standdartlaştırma işlemi yapacağız böylelikle hem kendi içerisinde hemde
# birbirleri arasında kıysalanabilir hale getirmiş olacağız. Bu metrikler 1 ile 5 arasında değişen skorlara çevrilip
# str veri tipine dönüştürülür. RFM değerleri str formatında yan yana toplanarak RFM skorları oluşmaktadır.

#               R       F       M       RFM     Segmentler
# Muşteri1      1       4       5       145     At Risk
# Müşteri2      4       5       4       454     Loyal Customers
# Müşteri3      5       1       3       513     New Customers

# Skorlar Üzerinden Segmentler Oluşturmak?
# => Segment oluşturmamızın temel sebebi daha az sayıda RFM sokoru oluşturmak ve okunabilirliği artırmak istememizdir.
# Çünkü yorum ve analiz yapmamız kolay olacaktır.

# Bilgi: RFM analizinin temeli basit pandas operasyonlarıdır.
###############################################################

# 1. İş Problemi (Business Problem)
# 2. Veriyi Anlama (Data Understanding)
# 3. Veri Hazırlama (Data Preparation)
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
# 7. Tüm Sürecin Fonksiyonlaştırılması

###############################################################
# 1. İş Problemi (Business Problem)
###############################################################

# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.

# Veri Seti Hikayesi
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler
#
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.


###############################################################
# 2. Veriyi Anlama (Data Understanding)
###############################################################

import datetime as dt # burada datetiem kütphanesi programa dahil edildi. amacımız fatura tarihi ve zamanı ile ilgili
# işlemler yapacağımız için bu kütüphane lazım olacaktır.
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option("display.width", 500)
# pd.set_option('display.max_rows', None) # bunu kullanmak istemedik. çünkü gözlem sayısının çok olmasından dolayı
# çalışırken zorluk çıkarabilir.
pd.set_option('display.float_format', lambda x: '%.3f' % x) # buurada ise, veri seti içerisinde yer alan float tipindeki
# değerlerin gösteri sırasında noktadan sonra kaç basamak gösterileceğini ifade etti. Bu kodda 3 basamak gösterilecek.

df_ = pd.read_excel("Miuul/CRM/online_retail_II.xlsx",
                    sheet_name="Year 2009-2010") # burada df_ isimli değişkene read_excel
# fonksiyonunu kullanark "online_retail_II.xlsx" isimli excel dosyasının sayfa ismi = Year 2009-2010 olan sayfasında
# yer alan veriler atandı.
df = df_.copy() # yukarıda okuyup df_ değişkenine atadığımız verinin kopysaını alarak df isimli değişkene atadık.
# amacımız, eğer verinin üzerinde geri dönüşü olmayan işlemler yaparsak veriyi bozarsak df_ isimli deüğişkenden orjinal
# halinden tekrar okuma yapmak yerine ( bu durum veri seti büyük olduğu için okuma süresi artıyor) direk kopya olan df
# den okuma yaparak işimizi hem hızlandırmış oluruz hemde verinin orjinal halini bozmamış oluruz.

df.head()

df.shape # df in boyut bilgilerine baktık.

df.isnull().sum() # değişkenlerde yer alan boş değerlerin toplamına baktık.


df["Description"].nunique() # ürün isimlerinin toplam eşsiz değer sayısını bulduk. eşsiz ürün sayısını bulduk.

df["Description"].value_counts().head() # her bir üründen kaçar tane satıldığını bulduk.

df.groupby("Description").agg({"Quantity": "sum"}).head() # bu kod hata verecektir. sebebi ise C kodlu satınalma
# iptalller vardır. bu iptaller de para iadesi olduğu için sonuç eksi çıkacaktır. ama bu durumu düzeltecek kod ilerleyen
# yerlerde gösterilecektir.

df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity",
                                                               ascending=False).head() # ürün açıklaması
# bazında kırılım gerçekleştirildi. daha sonra bu groupby üzerine agg fonksiyonu ile içerisinde yer alan işlemleri
# uyguladık. ascending = False ile

df["Invoice"].nunique() # invoice sınıfına ait eşsiz sınıf sayısını bulduk

df["TotalPrice"] = df["Quantity"] * df["Price"] # burada fatura başına ne kadar pra kazanıldığını hesapladık. bunu da
# yeni bir "TotalPrice" değişkenine atadık.

df.groupby("Invoice").agg({"TotalPrice": "sum"}).head() # burada fatura başına kaç para ödendiğini hesapladık.

df.groupby(["Invoice", "InvoiceDate"]).agg({"TotalPrice": "sum"}).sort_values("TotalPrice", ascending=False) # burada
# şunu yaptık: fatura numarasına ve fatura tarihine göre kırılım yaparak totol price üzerine agg ile sum uyguladık.
# çıkan sonucu da total prize a göre büyükten küçüğe sıraladık.

###############################################################
# 3. Veri Hazırlama (Data Preparation)
###############################################################

df.shape #  veri setinin boyut bilgisini aldık

df.isnull().sum() # veri setinde toplam kaç tane boş değer var onu hesapladık.

df.describe().T # veri setinin betimsel özelliklerini hesapladık.

df = df[(df['Quantity'] > 0)] # df içerisinden satış adedi sıfırdan büyük olan satışları seçip onu tekrar df değişkenine
# atadık. bunu yapmamızın sebebi ise satınalma idaleri veri setinden atmak.

df.dropna(inplace=True) # veri seti içerisinde yer alan boş değerleri dropna ile veri setinden attık ve bunu
# inplace=True ifadesi ile kalıcı hale getirdik. atamamızın en temel sebebi ise müşteri ID bilinmiyorsa müşteri özelide
# bir segmentasyon yapamayacağımız için boş gözlemler bizim için önem arz etmemektedir.

df[df["Invoice"].str.contains("C", na=False)] # burada df içerisinde C olanları seçtik.

df = df[~df["Invoice"].str.contains("C", na=False)] # burada df içerisinden str tipinde olan C ifadesini içermeyen
# gözlemler dışındaki değişkenleri seç ve tekrar df e atadık.

df= df[df["Invoice"].str.contains("C", na=False)] # burada df içerisinden str tipinde olan C ifadesini içeren
# gözlemler dışındaki değişkenleri seç ve tekrar df e atadık.

###############################################################
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
###############################################################

# Recency, Frequency, Monetary değerlerini her bir müşteri özelinde hesaplmaktır.

df.head()

df["InvoiceDate"].max() # burada en son fatura tarihini tespit ettik. yani en son satın alma tarihini tespit ettik.

today_date = dt.datetime(2010, 12, 11) # burada ise analizin yapıldığı tarih belirlendi. son satın alma tarihine 2 gün
# eklenerek bu analiz tarihi oluşturuldu.

type(today_date)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     'Invoice': lambda Invoice: Invoice.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})
# yukarıda ki kodda şu yapılmıştır: müşteri numarasına bilgisine ( 'Customer ID' ) göre kırılım yapılıyor önce bu
# kırılım sayesinde ana df de çoklu durumda olan customer ID ler yani aynı Customer ID den bir den fazla şekilde
# göründüğü için bu kırılım yapılarak çoklu durumda ki customer ID tekilleştirilmiş oldu. Teke indirilmiş oldu.

# 'InvoiceDate' (Recency): lambda InvoiceDate: (today_date - InvoiceDate.max()).days kodunda
# fatura satın alma tarihi hesaplanmıştır. bugünün tarihinden yani analizin yapıldığı tarihten son satınalma tarihi
# (InvoiceDate.max())) çıkarılmış ve bu çıkan tarihi de days ifadesi ile gün cinsinden yazdırılmıştır. Yani Recency
# hesaplamış olduk.

#  (Frequency) lambda Invoice: Invoice.nunique() kodunda ise Invoice değişkeninin eşsiz sınıf sayısını yani kaç tane
#  farklı fatura  var onları hesapla dedik. Frequency hesaplamış olduk.

#(monetary)lambda TotalPrice: TotalPrice.sum() kodunda ise toplam tutarı hesapla dedik. Yani monetary i hesaplamış olduk

rfm.head()

rfm.columns = ['recency', 'frequency', 'monetary'] # burada rfm data frame inin colonlarının isimleri bu liste
# içerisinde verilen sıraya göre sırası ile değiştirilmiş oldu.

rfm.describe().T # rfm data frame nin betimsel özelliklerine bakıldı.

rfm = rfm[rfm["monetary"] > 0] # burada rfm data frame nin içersinde yer alan monetary değerinin sıfırdan büyük olanları
# seç ve tekrar rfm değerine ata demiş olduk. bunu yapmamızdaki amaç ise iadelerden kaynaklı eksi değerleri almamaktır.

rfm.shape

# artık yeni veri setimiz rfm oldu. artık bunun üzerinden işlemler yapacağız.

###############################################################
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
###############################################################

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1]) # burada qcut fonksiyonu ile çeyrek değerlere
# göre bölme işlemi yaptık. amacmız bu bölme işlemi ile elde ettiğimiz çeyrekliklere labels içerisinde yer alan etik
# bilgilerini atayacağız. qcut fonksiyonu kısaca şunu yapar: ilk argüman bana böleceğim değişkenin ismin ver
# (rfm['recency']), ikinci argüman kaça böleceğimin bilgisini ver (5), böldükten sonra bunlara atayacağım etiket
# bilgisini ver (labels=[5, 4, 3, 2, 1]). burada qcut parçalara böler küçükten büyüğe doğru sıralar. burada listeyi
# büyükten küçüğe doğru yazmamızın amacı ise recency değerleri arasında ters ilişki olmasından dolayıdır. küçük parçaya
# büyük etiket numarası atanmıştır.

# 0-100, 0-20, 20-40, 40-60, 60-80, 80-100

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]) # burada yukarıda
# olduğu gibi qcut fonksiyonu belirttiğimiz değişkeni böldü ve labels listesi içerisinde yer alan etiket bilgilerine
# atama yaptı. ama burada rank(method="first") ifadesi olmadan çalıştırdığımızda kod hata verecektir. Valueerror
# verecektir. Bu hata şu demektir: öyle bir durum oluşmuş ki parçalara ayırıdğı zaman hem ilk parça da hemde diğer
# parçalarda aynı etiket numarası denk gelmiş. bu durum çok fazla gözlem olmasından kaynaklanmış. çok fazla tekrar eden
# frekans olmasından kaynaklanmış. küçükten büyüğe sıralandığında çeyrek değerlere düşen değerler aynı olmuştur. bu
# durumu çözmek için rank(method="first") ifadesi ile ilk gördüğünü ilk sınıfa ata demiş olduk.

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5]) # burada rencency de olduğu gibi bölüm
# işlemi ve etiket atam işlemi yapıldı.

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))
# yukarıda ki kodda ise elde ettiğimiz bu R,F,M değerlerini daha doğrusu R ve F değerlerini str tipinde yan yana
# toplayarak RFM_Skoru nu oluşturmamız gerekli.

rfm.describe().T

rfm[rfm["RFM_SCORE"] == "55"] # burada RFM skoru 55 olanları seçtik.

rfm[rfm["RFM_SCORE"] == "11"] # burada RFM skoru 11 olanları seçtik.

###############################################################
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
###############################################################
# regex => bu ifadeyi araştır mutlaka

# RFM isimlendirmesi
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
# yukarıda yer alan seg_map sözlüğü ile RFM skorlarına ait isimlendirme yaptık. bunun temel amacı ise okunabilirliği
# artırmak daha da tekilleştirebilmektir. yukarıdaki sözlüğü kısaca açıklarsak:
# bu seg_map ifadesi replace fonksiyonuna gönderildiğinde aşağıdaki gibi davranacaktır.
# r'[1-2][1-2]': birinci elemanda 1 yada 2 yi, ikinci elemanda 1 yada 2 yi görürsen 'hibernating' ifadesi ile değiştir.
# r'[1-2]5': : birinci elemanda 1 yada 2 yi, ikinci elemanda ise 5 i görürsen 'cant_loose' ifadesi ile değiştir.
# r'3[1-2]': birinci elemanda 3 ü, ikinci elemanda 1 yada 2 yi görürsen 'about_to_sleep' ifadesi ile değiştir.
# r'33': birinci elemanda 3 ü, ikinci elemanda 3 ü görürsen 'need_attention' ifadesi ile değiştir.
# şeklindedir.

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True) # burada replace metodu ile rfm veri seti içersinde yer
# alan RFM_SCORE değişkeninin yerine replace içerisinde yer alan seg_map sözlüğünde tanımlanan ifadeler ile değiştir
# dedik. regex=True ifadesi ile de skorları birleştimiş olacağız. en son olarak da bu işlemi rfm içersine segment
# isminde yeni bir değişken açarak rfm veri setine atamış olduk.

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"]) # burada "segment",
# "recency", "frequency", "monetary" değerleri rfm veri seti içerisinden seçilerek segment krılımında groupby ı alınarak
# bu seçilen değişkenlere agg fonksiyonu ile sırası ile mean ve count fonksiyonları uygulanmıştır.

rfm[rfm["segment"] == "cant_loose"].head() # burada rfm veri seti içerisinde yer alan segment değişkeninin cant loose
# a eşit olanları seçip ilk ,0,5 gözlemine baktık.

rfm[rfm["segment"] == "cant_loose"].index # burada rfm veri seti içerisinde yer alan segment değişkeninin cant loose a
# eşit olanların index bilgisine ulaştık.

new_df = pd.DataFrame() # burada new_df isminde bir değişken tanımladık ve bu değişkene ise pandas kütüphanesinin
# DataFrame fonskiyonu kullanrak bunu data frame e çevirdik.

new_df["new_customer_id"] = rfm[rfm["segment"] == "new_customers"].index # bu yeni new_df data frame mine
# new_customer_id isminde bir değişken ekledik ve bu değişkene ise rfm veri setinin segmentlerinin index bilgilerini
# atadık.

new_df["new_customer_id"] = new_df["new_customer_id"].astype(int) # bu yeni new_customer_id float olan tipini ise astype
# ile int e çevirdik.

new_df.to_csv("new_customers.csv") # burada elde ettiğimiz new_customes_id leri new_df veri seti içerisinden
# new_customer.csv ismi ile csv formatına çeririp dıaşrı çıkarıyoruz.

rfm.to_csv("rfm.csv") # burada ise rfm i csv formatında dışarı çıkarıyoruz.

###############################################################
# 7. Tüm Sürecin Fonksiyonlaştırılması
###############################################################

def create_rfm(dataframe, csv=False):

    # VERIYI HAZIRLAMA
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True) # burada boş değerleri(eksik) veri seti içerisinden attık.
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)] # C içeren değler veri seti

    # RFM METRIKLERININ HESAPLANMASI
    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ['recency', 'frequency', "monetary"]
    rfm = rfm[(rfm['monetary'] > 0)]

    # RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

    # cltv_df skorları kategorik değere dönüştürülüp df'e eklendi
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))


    # SEGMENTLERIN ISIMLENDIRILMESI
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm = rfm[["recency", "frequency", "monetary", "segment"]]
    rfm.index = rfm.index.astype(int)

    if csv:
        rfm.to_csv("rfm.csv")

    return rfm

df = df_.copy()

rfm_new = create_rfm(df, csv=True)










