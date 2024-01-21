# genetik_algoritma.py
from geopy.distance import geodesic
import random
import copy

class GenetikAlgoritma:
    def __init__(self, pop_boyutu, iterasyon_sayisi, caprazlama_orani, mutasyon_orani, noktalar, mesafe_matrisi):
        self.pop_boyutu = pop_boyutu
        self.iterasyon_sayisi = iterasyon_sayisi
        self.caprazlama_orani = caprazlama_orani
        self.mutasyon_orani = mutasyon_orani
        self.noktalar = noktalar
        self.mesafe_matrisi = mesafe_matrisi
        self.populasyon = self.init_populasyon()

    def init_populasyon(self):
        populasyon = []
        for _ in range(self.pop_boyutu):
            yol = list(range(len(self.noktalar)))
            random.shuffle(yol)
            populasyon.append(yol)
        return populasyon

    def mesafe_hesapla(self, rota):
        mesafe = 0
        for i in range(len(rota) - 1):
            mesafe += self.mesafe_matrisi[rota[i]][rota[i + 1]]
        mesafe += self.mesafe_matrisi[rota[-1]][rota[0]]
        return mesafe

    def uygunluk_hesapla(self, birey):
        return 1 / (self.mesafe_hesapla(birey) + 1e-10)

    def caprazla(self, ebeveyn1, ebeveyn2):
        nokta1 = random.randint(0, len(ebeveyn1) - 1)
        nokta2 = random.randint(nokta1, len(ebeveyn1) - 1)
        cocuk = [None] * len(ebeveyn1)
        cocuk[nokta1:nokta2] = ebeveyn1[nokta1:nokta2]
        for i in range(len(ebeveyn2)):
            if ebeveyn2[i] not in cocuk:
                for j in range(len(cocuk)):
                    if cocuk[j] is None:
                        cocuk[j] = ebeveyn2[i]
                        break
        return cocuk

    def mutasyon(self, birey):
        nokta1 = random.randint(0, len(birey) - 1)
        nokta2 = random.randint(0, len(birey) - 1)
        birey[nokta1], birey[nokta2] = birey[nokta2], birey[nokta1]
        return birey

    def yeni_nesil_olustur(self):
        uygunluklar = [self.uygunluk_hesapla(birey) for birey in self.populasyon]
        yeni_nesil = []

        for _ in range(self.pop_boyutu):
            ebeveyn1, ebeveyn2 = random.choices(self.populasyon, weights=uygunluklar, k=2)
            if random.random() < self.caprazlama_orani:
                cocuk = self.caprazla(ebeveyn1, ebeveyn2)
            else:
                cocuk = copy.deepcopy(random.choice([ebeveyn1, ebeveyn2]))
            if random.random() < self.mutasyon_orani:
                cocuk = self.mutasyon(cocuk)
            yeni_nesil.append(cocuk)

        self.populasyon = yeni_nesil

    def en_iyi_rota(self):
        uygunluklar = [self.uygunluk_hesapla(birey) for birey in self.populasyon]
        en_iyi_index = uygunluklar.index(max(uygunluklar))
        return self.populasyon[en_iyi_index], 1 / uygunluklar[en_iyi_index]

    def optimize_et(self):
        for _ in range(self.iterasyon_sayisi):
            self.yeni_nesil_olustur()

        en_iyi_rota, en_iyi_uygunluk = self.en_iyi_rota()
        return en_iyi_rota, en_iyi_uygunluk

    