import json, time
import numpy as np
import matplotlib.pyplot as plt

# puan çaarpanları
hiz_carpani = 1
aci_carpani = 1
uzaklik_carpani = 1
ivme_carpani = 1

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
    uzaklik_farki = []
    ilger_x = ilger[0]["x"]
    ilger_y = ilger[0]["y"]
    ilger_z = ilger[0]["z"]

    for hedef in hedefs:
        hedef_x = hedef["x"]
        hedef_y = hedef["y"]
        hedef_z = hedef["z"]
        uzaklik_farki.append = (((ilger_x - hedef_x) ** 2) + ((ilger_y - hedef_y) ** 2) + ((ilger_z - hedef_z) ** 2)) ** 0.5

        return uzaklik_farki
        
# iki uçak arasındaki hız
def hiz():
    hedefs,ilger = parametre_alma()
    hiz_farki = []
    ilger_hiz = ilger[0]["speed"]

    for hedef in hedefs:
        hedef_hiz = hedef["speed"]
        hiz_farki.append = ilger_hiz - hedef_hiz
        return hiz_farki
    

# iki uçak arasındaki açı
# bunu radyan mı normal mi alacaz bi kontrol et
def aci():
    aci_farki = []
    hedefs,ilger = parametre_alma()
    ilger_aci = ilger[0]["direction"]
    for hedef in hedefs:
        hedef_aci = hedef["direction"]
        aci_farki.append = ilger_aci - hedef_aci
        return aci_farki

# bi kaç saniyelik hoz takibi yapacaz ya da integrale girecez    
def ivme():
    ivme_farki = []
    hedefs,ilger = parametre_alma()
    
    
# puan sistemi oluşturulacak
def puan():
    hedefs = parametre_alma()
    toplam_puanlar_listesi = []
    aci_farki = aci()
    hiz_farki = hiz()
    uzaklik_farki = uzaklik()
    # ivme_farki = ivme()

    for i in hedefs:
        puan_degeri = (aci_farki * aci_carpani) + (hiz_farki * hiz_carpani) + (uzaklik_farki * uzaklik_carpani)# + (ivme_farki*ivme_carpani)
        toplam_puanlar_listesi.append({
            "id": i["id"],
            "puan": puan_degeri
        })
    
    return toplam_puanlar_listesi 




# main
while True:
    hiz_farki = hiz()
    uzaklik_farki = uzaklik()
    aci_farki = aci()
    toplam_puanlar_listesi = puan()  
    sirali_liste = (sorted(toplam_puanlar_listesi, key=lambda item: item["puan"]))
    secilen_hedef = sirali_liste[0]
    print(secilen_hedef)
    toplam_puanlar_listesi = []
    hiz_farki = []
    uzaklik_farki = []
    aci_farki = []
    time.sleep(1)
    
        
        
        
