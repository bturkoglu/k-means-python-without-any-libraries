
from Hesaplar import K_Mean_Hesap

from tkinter import *
from math import sin, cos, pi

from threading import Timer

class Cizim(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()

        self.canvas_width = 820
        self.canvas_height = 620
        
        self.renkler = self.renkAta()
        self.hesap = K_Mean_Hesap()

        self.yildiz_kose_sayisi = 5
        
        self.okunacak_alanlar= (('Nokta Adedi',self.hesap.nokta_adedi),
                                ('Küme Adedi', self.hesap.kume_adedi),
                                ('Random Çekirdeği', self.hesap.random_cekirdegi),
                                ('Yıldız Köşe Adedi', self.yildiz_kose_sayisi),
                                )
        
        self.okunan_degerler = {}


        self.merkez_yer = IntVar()
        
        self.tuslari_yap()

        self.canvas_noktalar = []
        self.canvas_merkezler = []
        self.canvas_dis_hatlar = []

        self.dongu = 0
        self.sonlandi = False

        self.slide_araligi = 0.5
        self.timer = RepeatedTimer(self.slide_araligi, self.hesabaDevam)

    def alanlari_oku(self):
        self.hesap.nokta_adedi = int(self.okunan_degerler['Nokta Adedi'].get())
        self.hesap.kume_adedi = int(self.okunan_degerler['Küme Adedi'].get())
        self.hesap.random_cekirdegi = int(self.okunan_degerler['Random Çekirdeği'].get())
        self.hesap.merkez_ilk_yer_tipi = self.merkez_yer.get()
        self.yildiz_kose_sayisi = int(self.okunan_degerler['Yıldız Köşe Adedi'].get())

    def tuslari_yap(self):
        #Ekranın soluna tuşlar için bir frame yapalım
        f = Frame(self, width=150,height = self.canvas_height, bd=8, relief=RAISED)
        f.pack(side=LEFT, fill=Y)
        
        # Entry'ler
        frmEntry = Frame(f, bd=3, relief=RAISED)
        frmEntry.pack(side=TOP)
        for alan in self.okunacak_alanlar:
            lab = Label(frmEntry, text=alan[0])
            ent = Entry(frmEntry, justify=CENTER, bd=3)
            ent.insert(0, alan[1])
            lab2 = Label(frmEntry, text= ' ')
            
            lab.pack(side=TOP)
            ent.pack(side=TOP,padx=5)
            lab2.pack(side=TOP)
            self.okunan_degerler[alan[0]]=ent


        #Butonlar
        frmButton = Frame(f, bd=3)
        frmButton.pack(side=TOP,pady= 10,fill=X)
        
        buttonpck = dict(pady=5,side=TOP, expand=YES, fill=X)
        
        b = Button(frmButton, text = 'Hesaba Başla', command = self.hesabaBasla)
        b.pack(**buttonpck)
        self.b = b
        
        b2 = Button(frmButton, text = 'Devam',
                    command = self.el_ile_Devam,
                    state = 'disabled')
        b2.pack(**buttonpck)
        self.b2 = b2

        slayt = Button(frmButton, text = 'Slayt',
                       command = self.slayt_basla,
                       state = 'disabled')
                       
        slayt.pack(**buttonpck)
        self.slayt = slayt


        b3 = Button(frmButton, text = 'Temizle',
                    command = self.temizlik,
                    state='disabled')
        b3.pack(**buttonpck)
        self.b3 = b3

        b4 = Button(frmButton, text = 'Çıkış',
                    command = self.quit)
        b4.pack(**buttonpck)

        # Radio
        frmRadio = Frame(f, relief=RAISED, bd = 3)
        frmRadio.pack(side=TOP, pady=10)
        Label(frmRadio,text='Merkez Başlangıç Yerleri').pack(side=TOP)
        v = IntVar()
        v.set(self.hesap.merkez_ilk_yer_tipi)
        for text, kod in self.hesap.merkez_ilk_yerler:
            b = Radiobutton(frmRadio, text=text, variable = v, value = kod)
            b.pack(anchor=W)

        self.merkez_yer = v

        # Bilgi
        l = Label(self, text = 'Bilgi: ', fg='red', bd=4, relief=RAISED)
        l.pack(side=TOP,fill=X)
        self.l = l
            
        #Canvas
        w = Canvas(self, width = self.canvas_width, height = self.canvas_height,
                   bd=8, relief=RAISED)
        w.pack()
        w.create_rectangle(15,15,815,615)
        self.w = w

        # Copyright
        l =Label(self, text = "\u00A9 2015 Her hakkı Bahaeddin TÜRKOĞLU'na aittir.", fg='red')
        l.pack(side =TOP, fill=X)
        
    def slayt_basla(self):
        self.timer.start()
        
    def stateler(self, s):
        if s == 1:            #Hesapla açık diğerleri kapalı
            self.b['state'] = 'normal'
            self.b2['state'] = 'disabled'
            self.b3['state'] = 'disabled'
            self.slayt['state'] = 'disabled'
        elif s == 2:            #Hesapla kapalı, diğerleri açık
            self.b['state'] = 'disabled'
            self.b2['state'] = 'normal'
            self.b3['state'] = 'normal'
            self.slayt['state'] = 'normal'
            
    def renkAta(self):
        return ('red','blue','orange','green','gray',
                'pink','deep sky blue','sea green','brown',
                'cyan','MediumPurple','MediumTurquoise',
                'magenta','maroon', 'lime green')
        

    def temizlik(self):
        self.dongu = 0
        self.sonlandi = False

        self.hesap.temizlik()
        
        self.noktalari_sil()
        self.merkezleri_sil()
        self.dis_hatlari_sil()

        self.l.config(text='Bilgi: ', fg='red')

        self.stateler(1)
        
    def hesabaBasla(self):
        self.temizlik()
        self.stateler(2)

        self.alanlari_oku()
        self.hesap.dataUret()
        self.hesap.noktalarin_merkezlerini_bul()
        self.ciz()

    def el_ile_Devam(self):
        if self.timer.is_running:
            self.timer.stop()
        self.hesabaDevam()
        
    def hesabaDevam(self):
        if self.sonlandi:
            self.timer.stop()
            return
        
        merkez_kaymasi = self.hesap.yeni_merkezleri_bul()

        if merkez_kaymasi < self.hesap.merkez_kayma_hassasiyeti:
            mesaj = 'Bilgi: Başarı ile %s döngüde sonuca ulaşıldı. (Merkez kayması: %.2f)'
            self.sonlandi = True
            renk = 'blue'
            self.timer.stop()
        else:
            self.dongu += 1
            mesaj = 'Bilgi: %s döngü. (Merkez kayması: %.2f)'
            renk = self.l['fg']

        mesaj = mesaj % (self.dongu, merkez_kaymasi)    
        self.l.config(text=mesaj, fg=renk)
    
        self.merkezleri_sil()
        self.merkezleri_ciz()
        
        self.hesap.noktalarin_merkezlerini_bul()
        self.noktalarin_renklerini_degistir()

        self.dis_hatlari_sil()
        self.dis_hatlari_ciz()

            
            
    def ciz(self):
        self.noktalari_ciz()
        self.merkezleri_ciz()
        self.dis_hatlari_ciz()
        
    def merkezleri_ciz(self):
        self.canvas_merkezler = []
      
        for i in range(self.hesap.kume_adedi):
            m = self.hesap.merkezler[i]
            x, y, r = m.x, m.y, self.renkler[i]
            yildiz = self.yildizUret(center_x=x, center_y=y)
            point = self.w.create_polygon(yildiz, fill=r,outline='red')
            self.canvas_merkezler.append(point)

            
    def merkezleri_sil(self):
        for i in self.canvas_merkezler:
            self.w.delete(i)
            

    def noktalari_ciz(self):
        self.canvas_noktalar = []
        for n in self.hesap.noktalar:
            x, y, r = n.x, n.y, self.renkler[n.kume]
            point = self.w.create_oval(x-3,y-3,x+3,y+3,fill=r)
            self.canvas_noktalar.append(point)
       
    def noktalarin_renklerini_degistir(self):
        for i in range(self.hesap.nokta_adedi):
            n = self.hesap.noktalar[i]
            r = self.renkler[n.kume]
            p = self.canvas_noktalar[i]
            self.w.itemconfig(p, fill=r)

    def noktalari_sil(self):
        for n in self.canvas_noktalar:
            self.w.delete(n)
        
            
    def dis_hatlari_ciz(self):
        self.canvas_dis_hatlar = []
        dis_hat = self.dis_hat_noktalar()
        for i in range(self.hesap.kume_adedi):
            r = self.renkler[i]
            p = dis_hat[i]
            dh = self.w.create_polygon(p, fill ='', width= 2, outline=r)
            self.canvas_dis_hatlar.append(dh)           
        
    def dis_hatlari_sil(self):
        for i in self.canvas_dis_hatlar:
            self.w.delete(i)
            
    def dis_hat_noktalar(self):
        dis_hat = []
        for i in range(self.hesap.kume_adedi):
            p = [(int(n.x),int(n.y)) for n in self.hesap.noktalar if n.kume == i]
            r = self.convex_hull(p)
            dis_hat.append(r)

        return dis_hat


    def kes(self, x):
        return int(round(x,0))

    def yildizUret(self, center_x=50, center_y=54,
                   inner_r=6, outer_r=15, kose=5):
        """
        Yıldızın köşe noktalarını hesaplar
        center_x, center_y: yıldızın merkezinin x ve y koordinatları
        inner_r, outer_r: yıldızın iç ve dış çapı
        kose : yıldızın köşe sayısı. Bizim yıldız 5 köşeli
        """
        kose = max(self.yildiz_kose_sayisi,2)
        points = []
        for i in range(kose * 2):
            angle = (2 * pi / kose) * i / 2
            r = inner_r if i % 2 == 0 else outer_r
            x = center_x + r * sin(angle)
            y = center_y + r * cos(angle)
            points.append(self.kes(x))
            points.append(self.kes(y))

        return points

    def convex_hull(self, points):
        """Computes the convex hull of a set of 2D points.
     
        Input: an iterable sequence of (x, y) pairs representing the points.
        Input örnek: [(2,3), (4,1), ....]
        
        Output: a list of vertices of the convex hull in counter-clockwise order,
          starting from the vertex with the lexicographically smallest coordinates.
        Implements Andrew's monotone chain algorithm. O(n log n) complexity.
        """
     
        # Sort the points lexicographically (tuples are compared lexicographically).
        # Remove duplicates to detect the case we have just one unique point.
        points = sorted(set(points))
     
        # Boring case: no points or a single point, possibly repeated multiple times.
        if len(points) <= 1:
            #return points
            return [(-2,0),(-1,0),(-1,1)]
     
        # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
        # Returns a positive value, if OAB makes a counter-clockwise turn,
        # negative for clockwise turn, and zero if the points are collinear.
        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
     
        # Build lower hull 
        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
     
        # Build upper hull
        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
     
        # Concatenation of the lower and upper hulls gives the convex hull.
        # Last point of each list is omitted because it is repeated at the beginning of the other list. 
        return lower[:-1] + upper[:-1]
 
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


if __name__ == '__main__':
    Cizim().mainloop()
