import numpy as np

def takip_ediyor_mu():
    # zaman_adimi=1.0 >> döngüde verilecek
    ilger,hedefs = parametre_alma()
    konum_ben = (ilger["x"], ilger["y"])
    hiz_ben = ilger["speed"]
    aci_ben = ilger["direction"]
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
            return True
        else:
            return False

        # Örnek kullanım:
        #aci_ben = np.deg2rad(0)  # doğuya doğru
        #aci_takipci = np.deg2rad(0)  # doğuya doğru
        #aci değerlerinin nasıl çıktığına bak
