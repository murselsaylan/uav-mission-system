import math

def waypoint_ver(konum, yarışma_merkez, yarışma_cap, yasaklı_bölgeler):
    def mesafe(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def daire_icinde(nokta, merkez, cap):
        return mesafe(nokta, merkez) <= cap

    en_yakin = None
    min_mesafe = float("inf")

    for x in range(yarışma_merkez[0] - yarışma_cap, yarışma_merkez[0] + yarışma_cap, 10):
        for y in range(yarışma_merkez[1] - yarışma_cap, yarışma_merkez[1] + yarışma_cap, 10):
            nokta = (x, y)
            if not daire_icinde(nokta, yarışma_merkez, yarışma_cap):
                continue
            yasakta = any(daire_icinde(nokta, (b["x"], b["y"]), b["cap"]) for b in yasaklı_bölgeler)
            if yasakta:
                continue
            uzaklik = mesafe(konum, nokta)
            if uzaklik < min_mesafe:
                min_mesafe = uzaklik
                en_yakin = nokta

    return en_yakin