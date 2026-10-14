import json, time, utils


# bilgileri katagorilere ayırma
ilger = []
kr = []
hava = []
hedefs = []
hedefEngel = []

def parametre_alma():
    with open("config\ihas.json") as file:
        datas = json.load(file)

    for data in datas:
        ids = (data["id"][:5])
        if ids == ("Hedef"):
            hedefs.append(data)
        if ids == ("hava_"):
            hava.append(data)
        if ids == ("kamik"):
            kr.append(data)
        if ids == ("ilger"):
            ilger.append(data)
    return hedefs,hava,kr,ilger
# daire çapları ve kesişme durumu

def hedef_listesi():
        hedefs,hava,kr,ilger = parametre_alma()
        for engel in hava:
            for hedef in hedefs:
                speedx = hedef["speed"]
                speedy = ilger[0]["speed"]# hız hesaplama
                hız = (((speedx - speedy) ** 2) ** -2) 
                if hız == 0:
                    hız = 1/2
                directionx = hedef["direction"]
                directiony = ilger[0]["direction"]
                if (((directionx - directiony) ** 2) ** -2) < 180:
                    directionz = (((directionx - directiony) ** 2) ** -2) / 90       
                if (((directionx - directiony) ** 2) ** -2) > 180:
                    directionz = (((360 - (directionx - directiony)) ** 2) ** -2) / 90 
                if (directionx - directiony) == 0:
                    directionz = 1/10
                if (((directionx - directiony) ** 2) ** -2) == 180:
                    directionz = 2
                vektor = directionz * hız
                if vektor == 0:
                    vektor = 1/2
                k = ((2 * engel["cap"]) / ((hedef["x"] - ilger[0]["x"]) + (hedef["y"] - ilger[0]["y"]))) ** -2
                yfark = (hedef["x"] - ilger[0]["x"]) * k / 2
                xfark = (hedef["y"] - ilger[0]["y"]) * k / 2
                x1 = engel["x"] - xfark
                x2 = engel["x"] + xfark
                y1 = engel["y"] - yfark
                y2 = engel["y"] + yfark
                a1 = y2 - y1
                b1 = x1 - x2
                c1 = a1 * x1 + b1 * y1
                a2 = hedef["y"] - ilger[0]["y"]
                b2 = ilger[0]["x"] - hedef["y"]
                c2 = a2 * ilger[0]["x"] + b2 * ilger[0]["y"]
                det = a1 * b2 - a2 * b1
                if det == 0:
                    çarp = 1 * vektor
                else:
                    x = (b2 * c1 - b1 * c2) / det
                    y = (a1 * c2 - a2 * c1) / det
                    if (min(x1, x2) <= x <= max(x1, x2) and min(ilger[0]["x"], hedef["x"]) <= x <= max(ilger[0]["x"], hedef["x"]) and min(y1, y2) <= y <= max(y1, y2) and min(ilger[0]["y"], hedef["y"]) <= y <= max(ilger[0]["y"], hedef["y"])):
                        çarp = 3 * vektor
                    else:
                        çarp = 1 * vektor
                hedefEngel.append({"id1": engel["id"], "id2": hedef["id"], "çarpan": çarp})
        return hedefEngel
       

while True:
    hedefEngel = []
    ilger = []
    kr = []
    hava = []
    hedefs = []
    
    hedefEngel=hedef_listesi()
    sirali_sozluk = (sorted(hedefEngel, key=lambda item: item["çarpan"]))
    for i in sirali_sozluk:
        print(i)
    secilen_hedef = sirali_sozluk[0]
    sirali_sozluk = []
    print(secilen_hedef["id2"][-1])
    utils.change_target_box(int(secilen_hedef["id2"][-1]))
    time.sleep(1)
    



        
        



        

