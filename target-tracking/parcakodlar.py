import numpy as np
import matplotlib.pyplot as plt

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

def aci_farki(aci1, aci2):
    # İki açı arasındaki farkı 0 ile 2*pi arasına çeker
    fark = (aci2 - aci1) % (2 * np.pi)
    return fark

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
            yay_aci = aci_farki(v1, v2)
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

    if aci_farki(yay_baslangic, yay_bitis) < np.pi:
        acilar = np.linspace(yay_baslangic, yay_bitis, 100)
    else:
        acilar = np.linspace(yay_baslangic, yay_bitis - 2*np.pi, 100)

    yay_x = merkez[0] + yaricap * np.cos(acilar)
    yay_y = merkez[1] + yaricap * np.sin(acilar)
    eksen.plot(yay_x, yay_y, 'r-')

    plt.legend()
    plt.show()

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

def yay_uzerinde_noktalar(merkez, yaricap, baslangic_aci, bitis_aci, adim_uzunlugu):
    """Çember yayı üzerinde belli aralıklarla noktalar oluşturur."""
    yay_uzunlugu = yaricap * aci_farki(baslangic_aci, bitis_aci)
    adim_sayisi = int(yay_uzunlugu / adim_uzunlugu)
    
    if aci_farki(baslangic_aci, bitis_aci) < np.pi:
        acilar = np.linspace(baslangic_aci, bitis_aci, adim_sayisi + 1)
    else:
        acilar = np.linspace(baslangic_aci, bitis_aci - 2*np.pi, adim_sayisi + 1)

    noktalar = []
    for aci in acilar[1:]:  # Başlangıç açısını eklememek için [1:]
        x = merkez[0] + yaricap * np.cos(aci)
        y = merkez[1] + yaricap * np.sin(aci)
        noktalar.append((x, y))
    return noktalar

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
            yay_aci = aci_farki(v1, v2)
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

# Kullanım
baslangic = (0, 0)
hedef = (10, 0)
merkez = (5, 2)
yaricap = 4

waypoints = rota_ciz_waypoints(baslangic, hedef, merkez, yaricap, adim_uzunlugu=0.5)

# Noktaları yazdıralım
for i, wp in enumerate(waypoints):
    print(f"Waypoint {i}: {wp}")

# İstersen görselle de çizelim:
xler, yler = zip(*waypoints)
plt.plot(xler, yler, 'o-', markersize=3)
plt.plot(merkez[0], merkez[1], 'rx')  # Çember merkezi
circle = plt.Circle(merkez, yaricap, color='red', fill=False)
plt.gca().add_patch(circle)
plt.axis('equal')
plt.grid(True)
plt.show()
rota_ciz(baslangic, hedef, merkez, yaricap)