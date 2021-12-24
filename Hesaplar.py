import random

class Nokta:
    def __init__(self, no, x, y):
        self.no = no
        self.x = x
        self.y = y
        self.kume = 0

    def __repr__(self):
        return 'N%s(%s, %s, %s)' % (self.no, int(self.x), int(self.y), self.kume)
    
class Merkez:
    def __init__(self, no, x, y):
        self.no = no
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Mrk%s(%s, %s)' % (self.no, int(self.x), int(self.y))

class K_Mean_Hesap:
    def __init__(self):
        self.noktalar = []
        self.merkezler = []

        self.nokta_adedi = 1000
        self.kume_adedi = 15

        self.x_min  = 20
        self.x_max  = 800
        self.y_min  = 20
        self.y_max  = 600

        self.merkez_ilk_yer_tipi = 1
        self.merkez_ilk_yerler = (('Noktalar Arasından',1),
                                  ('X-ekseni üzerinde', 2),
                                  ('Y-ekseni üzerinde',3),
                                  ('Merkezler Originde',4),
                                  ('Merkezler Ortada',5))
        
        self.merkez_kayma_hassasiyeti = 0.5
        self.merkez_kayma_max_sayisi = 500

        self.random_cekirdegi = 111
        
    def temizlik(self):
        self.noktalar = []
        self.merkezler = []
        
    def randomUret(self):
        x = int(random.uniform(self.x_min, self.x_max))
        y = int(random.uniform(self.y_min, self.y_max))
        return x,y

    def mesafeBul(self, a, b):
        mesafe = ((a.x - b.x)**2 + (a.y - b.y)**2)**.5
        return mesafe


    def kumeleriBas(self):
        for k in range(len(self.merkezler)):
            print('Kume:',self.merkezler[k])
            for n in self.noktalar:
                if n.kume == k: print('\t',n)

    def dataUret(self):

        random.seed(self.random_cekirdegi)

        self.temizlik()
        
        #noktaları üretelim.
        for i in range(self.nokta_adedi):
            x,y = self.randomUret()
            n = Nokta(i, x, y)
            self.noktalar.append(n)
            
            
        # Merkezlerin ilk yerleri
        
        if self.merkez_ilk_yer_tipi == 1:
            # Noktaların arasından kümeleri seçelim.
            merkez_noktalari = random.sample(self.noktalar, self.kume_adedi)
            for i in range(self.kume_adedi):
                n = merkez_noktalari[i]
                m = Merkez(i, n.x, n.y)
                self.merkezler.append(m)

        elif self.merkez_ilk_yer_tipi == 2:
            # x-ekseni üzerine yerleştirelim.
            adim = int((self.x_max - self.x_min)/self.kume_adedi)
            x = self.x_min
            y = self.y_min
            for i in range(self.kume_adedi):
                x += adim
                m = Merkez(i, x, y)
                self.merkezler.append(m)

        elif self.merkez_ilk_yer_tipi == 3:
            # y-ekseni üzerine yerleştirelim.
            adim = int((self.y_max - self.y_min)/self.kume_adedi)
            x = self.x_min
            y = self.y_min
            for i in range(self.kume_adedi):
                y += adim
                m = Merkez(i, x, y)
                self.merkezler.append(m)

        elif self.merkez_ilk_yer_tipi == 4:
            # Bütün merkezler originde olsun üzerine yerleştirelim.
            x = self.x_min
            y = self.y_min
            for i in range(self.kume_adedi):
                m = Merkez(i, x, y)
                self.merkezler.append(m)

        elif self.merkez_ilk_yer_tipi == 5:
            # Bütün merkezler ortada.
            x = int((self.x_max - self.x_min)/2)
            y = int((self.y_max - self.y_min)/2)
            for i in range(self.kume_adedi):
                m = Merkez(i, x, y)
                self.merkezler.append(m)


    def noktalarin_merkezlerini_bul(self):
       # Herbir noktanın merkezlere uzaklıkları bulunup, en yakın olana atanacak
        for n in self.noktalar:
            min_mesafe = 1e10
            min_merkez = -1
            for m in self.merkezler:
                mesafe = self.mesafeBul(n, m)
                if min_mesafe > mesafe:
                    min_mesafe = mesafe
                    min_merkez = m.no

                #print(n, m, 'mesafe:',mesafe)

            n.kume = min_merkez
            #print('Küme:', n.kume)
                
    def yeni_merkezleri_bul(self):
        # Küme içindeki noktaların merkezi bulunup, merkezler'in yerleri update edilecek.
        merkez_kaymasi = 0

        for k in range(self.kume_adedi):
            xler = [n.x for n in self.noktalar if n.kume == k]
            kume_eleman_sayisi = len(xler)
            if kume_eleman_sayisi > 0:
                yenix = sum(xler) / kume_eleman_sayisi
                yeniy = sum([n.y for n in self.noktalar if n.kume == k])/kume_eleman_sayisi

                merkez = self.merkezler[k]
                merkez_kaymasi += abs(merkez.x - yenix) + abs(merkez.y - yeniy)
                
                #print(merkezler[k], end=' ')
                self.merkezler[k].x = yenix
                self.merkezler[k].y = yeniy
                #print('Yeni yer:',merkezler[k])
            
            else:
                #print(k,'.merkezde eleman sayısı 0 çıktı')
                pass

        return merkez_kaymasi
                    
    def hesapla(self):
        
        for dongu in range(self.merkez_kayma_max_sayisi):
            
            self.noktalarin_merkezlerini_bul()

            merkez_kaymasi = self.yeni_merkezleri_bul()

            #print('Merkez_kayması', merkez_kaymasi)
            if merkez_kaymasi < self.merkez_kayma_hassasiyeti:
                print('Başarı ile',dongu+1,' döngüde sonuca ulaşıldı.')
                break
        else:
            print(self.merkez_kayma_max_sayisi,' kez merkez kaydırıldı ama tam sonuca ulaşılamadı.')

if __name__ == '__main__':
    hesap = K_Mean_Hesap()
    hesap.dataUret()
    hesap.hesapla()

    hesap.kumeleriBas() 
    
