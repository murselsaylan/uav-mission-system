import json, time, utils
import numpy as np
import matplotlib.pyplot as plt

# bilgileri katagorilere ayırma
ilger = []
kr = []
havas = []
hedefs = []
secilen_hedef = () # şu anlık sembolik 

# json dosyasından veri çekmek ve katagorize etmek
def parametre_alma():
    with open("config\ihas.json") as file:
        datas = json.load(file)

    for data in datas:
        ids = (data["id"][:5])
        if ids == ("Hedef"):
            hedefs.append(data)
        if ids == ("hava_"):
            havas.append(data)
        if ids == ("kamik"):
            kr.append(data)
        if ids == ("ilger"):
            ilger.append(data)
    return hedefs,havas,kr,ilger

# iki uçak arasındaki mesafe
def uzaklik():
    hedefs,ilger = parametre_alma()
    ilger_x = ilger[0]["x"]
    ilger_y = ilger[0]["y"]
    ilger_z = ilger[0]["z"]

    for hedef in hedefs:
        hedef_x = hedef["x"]
        hedef_y = hedef["y"]
        hedef_z = hedef["z"]
        uzaklik_ucak = (((ilger_x - hedef_x) ** 2) + ((ilger_y - hedef_y) ** 2) + ((ilger_z - hedef_z) ** 2)) ** 0.5

        return uzaklik_ucak
        
# iki uçak arasındaki hız
def hiz():
    hedefs,ilger = parametre_alma()
    ilger_hiz = ilger[0]["speed"]

    for hedef in hedefs:
        hedef_hiz = hedef["speed"]
        hiz_farki = ilger_hiz - hedef_hiz
        return hiz_farki
    

# iki uçak arasındaki açı
# bunu radyan mı normal mi alacaz bi kontrol et
def aci():
    hedefs,ilger = parametre_alma()
    ilger_aci = ilger[0]["direction"]
    for hedef in hedefs:
        hedef_aci = hedef["direction"]
        aci_farki = ilger_aci - hedef_aci
        return aci_farki

# seçilen hedefle ilgerin arası kontrol edilecek
# puanlanma sistemi tamamladığında devamı yazlılacak
# bu fonksiyon sadece hava savunmanın içindemiyiz diye kontrol ediyor rota üzerinde hava savunmanın olduğu kod aşağıda   
def hava_savunma():
    havas,ilger,hedefs = parametre_alma()
    ilger_x = ilger[0]["x"]
    ilger_y = ilger[0]["y"]
    hava_tehlike = True

##############################################

    for hava in havas:
        hava_x = hava["x"]
        hava_y = hava["y"]
        hava_cap = hava["cap"]
        uzaklik_hava = ((ilger_x - hava_x) ** 2) + ((ilger_y - hava_y) ** 2) ** 0.5

        if (uzaklik_hava > hava_cap):
            hava_tehlike = True
            return hava_tehlike
        
        else:
            hava_tehlike = False
            return hava_tehlike
        
# seçilen hedeften sonra
def iki_nokta_arasi_cember_iceriyor_mu():

    ilger,havas = parametre_alma()
    # Başlangıç ve hedef arasındaki mesafeyi hesapla
    mesafe = np.hypot(secilen_hedef["x"] - ilger[0]["x"], secilen_hedef["y"] - ilger[0]["y"])
    
    # Eğer iki nokta arasındaki mesafe, çemberin çapından küçükse (yarıçap*2), o zaman çember içinde
    for hava in havas:
        if mesafe <= 2 * hava["cap"]:
            engel_durumu = True
            return engel_durumu  # Çember iki nokta arasında yer alıyor
        engel_durumu = False
        return engel_durumu  # Çember iki nokta arasında yer almıyor

# yarışma alanının çapı için
# rota durumlarına bakılacak en mantıklısı tüm rota değiştirme durumları için >> tüm alan - hava savunmaları >> en yakın nokta = waypoint
def guvenli_alan():
    ilger = parametre_alma()
    ilger_x = ilger[0]["x"]
    ilger_y = ilger[0]["y"]
    merkez_x = 0 # emreye sor
    merkez_y = 0 
    merkez_cap = 1000
    guvenli_tehlike = None
    uzaklik_guvenli = ((ilger_x - merkez_x) ** 2) + ((ilger_y - merkez_y) ** 2) ** 0,5

    if (merkez_cap < uzaklik_guvenli):
        guvenli_tehlike = True
        return guvenli_tehlike
    else:
        guvenli_tehlike = False
        return guvenli_tehlike

# arkamızda bizi takip eden uçak var mı
# döngüden sonra doldurulmalı
def kacis_kontrol():
    # zaman_adimi=1.0 >> döngüde verilecek
    ilger,hedefs = parametre_alma()
    konum_ben = (ilger[0]["x"], ilger[0]["y"])
    hiz_ben = ilger[0]["speed"]
    aci_ben = ilger[0]["direction"]
    for hedef in hedefs:
        konum_takipci = (hedef["x"], hedef["y"])
        hiz_takipci = hedef["speed"]
        aci_takipci = hedef["direction"]
        """
        Bir uçağın bizi takip edip etmediğini kontrol eder.
        konum_ben: (x, y) bizim konumumuz
        hiz_ben: bizim hızımız (m/s)
        aci_ben: bizim yönümüz (radyan cinsinden)
        konum_takipci: (x, y) takipçi uçağın konumu
        hiz_takipci: takipçi uçağın hızı
        aci_takipci: takipçi uçağın yönü
        zaman_adimi: kaç saniye sonra kontrol edelim (default 1 saniye)
        """

        # Şu anki mesafeyi ölç
        baslangic_mesafe = np.linalg.norm(np.array(konum_ben) - np.array(konum_takipci))
        
        # Zaman adımı sonrası bizim yeni konumumuz
        yeni_konum_ben = (
            konum_ben[0] + hiz_ben * np.cos(aci_ben) * zaman_adimi,
            konum_ben[1] + hiz_ben * np.sin(aci_ben) * zaman_adimi
        )

        # Zaman adımı sonrası takipçinin yeni konumu
        yeni_konum_takipci = (
            konum_takipci[0] + hiz_takipci * np.cos(aci_takipci) * zaman_adimi,
            konum_takipci[1] + hiz_takipci * np.sin(aci_takipci) * zaman_adimi
        )

        # Zaman adımı sonrası yeni mesafeyi ölç
        yeni_mesafe = np.linalg.norm(np.array(yeni_konum_ben) - np.array(yeni_konum_takipci))

        # Takipçi yönü bizim konumumuza ne kadar bakıyor, bunu ölçelim
        vektor_takipci = np.array([np.cos(aci_takipci), np.sin(aci_takipci)])
        vektor_hedef = np.array(konum_ben) - np.array(konum_takipci)
        vektor_hedef = vektor_hedef / np.linalg.norm(vektor_hedef)  # normalize
        
        acisal_fark = np.arccos(np.clip(np.dot(vektor_takipci, vektor_hedef), -1.0, 1.0))

        # Eğer açı küçükse (örneğin 30 dereceden küçükse) ve mesafe azalıyorsa takip ediyordur
        if np.degrees(acisal_fark) < 30 and yeni_mesafe < baslangic_mesafe:
            kacis = True
            return kacis
        else:
            kacis = False
            return kacis

        # Örnek kullanım:
        #aci_ben = np.deg2rad(0)  # doğuya doğru
        #aci_takipci = np.deg2rad(0)  # doğuya doğru
        #aci değerlerinin nasıl çıktığına bak

# döngü içinde komut vereceğiz
def yukseklik_kontrol(kr_gorev_basla):
    ilger = parametre_alma()
    ilger_z = ilger[0]["z"]

    if (kr_gorev_basla == True):
        return True
    else:
        if (ilger_z > 20):
            return True
        elif (20 => ilger_z > 10):
            print("Tehlikeli Yükseklik")
            return True
        else:
            return False

# öncelik sırası verilecek
# kaçış kontrol eklenecek
def rota():
    guvenli_tehlike = guvenli_alan()
    hava_tehlike = hava_savunma()
    kr_gorev_basla = kr_gorev()
    engel_durumu = iki_nokta_arasi_cember_iceriyor_mu()
    kacis = kacis_kontrol()

    if (guvenli_tehlike == True):
        # güvenli alana geri dönecek

    elif (guvenli_tehlike == False):
        # devam

        if (kr_gorev_basla == False):
            # true olduğu durum için bi daha uyarlamamız lazım

            if (hava_tehlike == True):
            # yükseklik artacak

            elif (hava_tehlike == False):
                # devam

                if (engel_durumu == True):
                    #çembersel rota

                elif (engel_durumu == False):
                    #düz rota

                    if (kacis == True):
                        # kaçış rotası oluşturulacak
                    
                    elif (kacis == False):
                        # düz rota


# döngü içinde komutla kontrol eldilip seçilen hedefi sabit kr olacak şekilde ayarla
def kr_gorev():
    kr = parametre_alma()
    kr_gorev_basla = None

    if (kr_gorev_basla == True):
        secilen_hedef = kr
        return secilen_hedef
    else:
        return

# puan sistemi oluşturulacak
def puan():

# seçilen hedeeften sonra
# ilgerle hedef arasında hava savunması varsa hava savunması üzerinden teğet noktalarla rota oluşturulur 
# şu anlık çap = hava savunma cap onu güvenli olacak şekilde 1-2 metre arttır
def teget_noktalarini_bul(nokta, merkez, yaricap):
    # Nokta ve merkez koordinatları
    nokta_x, nokta_y = nokta
    merkez_x, merkez_y = merkez

    # Noktanın merkeze uzaklığı
    mesafe = np.hypot(nokta_x - merkez_x, nokta_y - merkez_y)
    
    if mesafe < yaricap:
        raise ValueError("Nokta çemberin içinde, teğet bulunamaz.")
    
    # Açı ve düzeltmeler
    aci_merkez = np.arctan2(nokta_y - merkez_y, nokta_x - merkez_x)
    aci_offset = np.arccos(yaricap / mesafe)

    # İki teğet açısı
    aci_teget1 = aci_merkez + aci_offset
    aci_teget2 = aci_merkez - aci_offset

    # İki teğet noktası
    teget1 = (merkez_x + yaricap * np.cos(aci_teget1),
              merkez_y + yaricap * np.sin(aci_teget1))
    teget2 = (merkez_x + yaricap * np.cos(aci_teget2),
              merkez_y + yaricap * np.sin(aci_teget2))
    
    return teget1, teget2

# seçilen hedeften sonra
# hava savunma ile uçak arasındaki açı farkı
def aci_farki_hava(aci1, aci2):
    # İki açı arasındaki farkı 0 ile 2*pi arasına çeker
    fark = (aci2 - aci1) % (2 * np.pi)
    return fark

#seçilen hedeften sonra
# arada hava savunması var ise çizilecek rota 
# düzenlenesi gerek
def rota_ciz(baslangic, hedef, merkez, yaricap):
    # Teğet noktalarını bul
    baslangic_tegetleri = teget_noktalarini_bul(baslangic, merkez, yaricap)
    hedef_tegetleri = teget_noktalarini_bul(hedef, merkez, yaricap)

    en_iyi_mesafe = float('inf')
    secilen_tegetler = None

    for teget_a in baslangic_tegetleri:
        for teget_b in hedef_tegetleri:
            # A -> TeğetA düz çizgi
            yol1 = np.linalg.norm(np.array(baslangic) - np.array(teget_a))
            # TeğetA -> TeğetB yay çizgisi
            v1 = np.arctan2(teget_a[1]-merkez[1], teget_a[0]-merkez[0])
            v2 = np.arctan2(teget_b[1]-merkez[1], teget_b[0]-merkez[0])
            yay_aci = aci_farki_hava(v1, v2)
            yay_mesafe = yaricap * yay_aci
            # TeğetB -> B düz çizgi
            yol2 = np.linalg.norm(np.array(teget_b) - np.array(hedef))

            toplam_yol = yol1 + yay_mesafe + yol2

            if toplam_yol < en_iyi_mesafe:
                en_iyi_mesafe = toplam_yol
                secilen_tegetler = (teget_a, teget_b)

    # Seçilen teğetler
    teget_a, teget_b = secilen_tegetler

    # Çizim başlar
    fig, eksen = plt.subplots()
    eksen.set_aspect('equal')
    eksen.grid(True)

    # Çember
    cember = plt.Circle(merkez, yaricap, color='red', fill=False)
    eksen.add_artist(cember)

    # Noktalar
    eksen.plot(baslangic[0], baslangic[1], 'go', label='Başlangıç')
    eksen.plot(hedef[0], hedef[1], 'bo', label='Hedef')
    eksen.plot([baslangic[0], teget_a[0]], [baslangic[1], teget_a[1]], 'g--')
    eksen.plot([hedef[0], teget_b[0]], [hedef[1], teget_b[1]], 'b--')

    # Yay çiz
    yay_baslangic = np.arctan2(teget_a[1]-merkez[1], teget_a[0]-merkez[0])
    yay_bitis = np.arctan2(teget_b[1]-merkez[1], teget_b[0]-merkez[0])

    if aci_farki_hava(yay_baslangic, yay_bitis) < np.pi:
        acilar = np.linspace(yay_baslangic, yay_bitis, 100)
    else:
        acilar = np.linspace(yay_baslangic, yay_bitis - 2*np.pi, 100)

    yay_x = merkez[0] + yaricap * np.cos(acilar)
    yay_y = merkez[1] + yaricap * np.sin(acilar)
    eksen.plot(yay_x, yay_y, 'r-')

    plt.legend()
    plt.show()

# seçilen hedeften sonra
# rota üzerinden noktalar oluşturma düz rotalar için
# düzenlenmesi gerek

def iki_nokta_arasi_noktalar(nokta1, nokta2, adim_uzunlugu):
    """İki düz nokta arasında belli aralıklarla noktalar oluşturur."""
    x1, y1 = nokta1
    x2, y2 = nokta2
    mesafe = np.hypot(x2 - x1, y2 - y1)
    adim_sayisi = int(mesafe / adim_uzunlugu)
    noktalar = []
    for i in range(1, adim_sayisi + 1):
        oran = i * adim_uzunlugu / mesafe
        yeni_x = x1 + (x2 - x1) * oran
        yeni_y = y1 + (y2 - y1) * oran
        noktalar.append((yeni_x, yeni_y))
    return noktalar

# seçilen hedeften sonra
# rota üzerinden noktalar oluşturma çembersel rotalar için
# düzenlenmesi gerek

def yay_uzerinde_noktalar(merkez, yaricap, baslangic_aci, bitis_aci, adim_uzunlugu):
    """Çember yayı üzerinde belli aralıklarla noktalar oluşturur."""
    yay_uzunlugu = yaricap * aci_farki_hava(baslangic_aci, bitis_aci)
    adim_sayisi = int(yay_uzunlugu / adim_uzunlugu)
    
    if aci_farki_hava(baslangic_aci, bitis_aci) < np.pi:
        acilar = np.linspace(baslangic_aci, bitis_aci, adim_sayisi + 1)
    else:
        acilar = np.linspace(baslangic_aci, bitis_aci - 2*np.pi, adim_sayisi + 1)

    noktalar = []
    for aci in acilar[1:]:  # Başlangıç açısını eklememek için [1:]
        x = merkez[0] + yaricap * np.cos(aci)
        y = merkez[1] + yaricap * np.sin(aci)
        noktalar.append((x, y))
    return noktalar

# seçilen hedeften sonra
# anlık rotaları sıralı halde oluşturmak toplam rota gibi bir şey
# kontrol edilmeli
def rota_ciz_waypoints(baslangic, hedef, merkez, yaricap, adim_uzunlugu=0.5):
    # Teğet noktalarını bul
    baslangic_tegetleri = teget_noktalarini_bul(baslangic, merkez, yaricap)
    hedef_tegetleri = teget_noktalarini_bul(hedef, merkez, yaricap)

    en_iyi_mesafe = float('inf')
    secilen_tegetler = None

    for teget_a in baslangic_tegetleri:
        for teget_b in hedef_tegetleri:
            yol1 = np.linalg.norm(np.array(baslangic) - np.array(teget_a))
            v1 = np.arctan2(teget_a[1]-merkez[1], teget_a[0]-merkez[0])
            v2 = np.arctan2(teget_b[1]-merkez[1], teget_b[0]-merkez[0])
            yay_aci = aci_farki_hava(v1, v2)
            yay_mesafe = yaricap * yay_aci
            yol2 = np.linalg.norm(np.array(teget_b) - np.array(hedef))
            toplam_yol = yol1 + yay_mesafe + yol2

            if toplam_yol < en_iyi_mesafe:
                en_iyi_mesafe = toplam_yol
                secilen_tegetler = (teget_a, teget_b)

    teget_a, teget_b = secilen_tegetler

    # Noktaları oluştur
    noktalar = []
    noktalar += iki_nokta_arasi_noktalar(baslangic, teget_a, adim_uzunlugu)
    noktalar += yay_uzerinde_noktalar(merkez, yaricap,
                                      np.arctan2(teget_a[1]-merkez[1], teget_a[0]-merkez[0]),
                                      np.arctan2(teget_b[1]-merkez[1], teget_b[0]-merkez[0]),
                                      adim_uzunlugu)
    noktalar += iki_nokta_arasi_noktalar(teget_b, hedef, adim_uzunlugu)

    # Başlangıç noktasını da listeye ekliyoruz
    noktalar.insert(0, baslangic)
    # Hedef noktasını da sonuna ekliyoruz
    noktalar.append(hedef)

    return noktalar

# seçilen hedeften sonra
# Kullanım
# burayı bir daha uyarla
baslangic = (ilger["x"], ilger["y"])
hedef = (secilen_hedef["x"], secilen_hedef["y"])
for hava in havas:
    merkez = (hava["x"], hava["y"])
    yaricap = hava["cap"]


