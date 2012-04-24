import pygame
import random
import time

k_czarny=(0,0,0)
k_bialy=(255,255,255)
k_czerwony=(255,0,0)
k_zielony=(0,255,0)
k_niebieski=(0,0,255)

szerokosc_ekranu=800
wysokosc_ekranu=600

#####################################################################

def ustaw_ikone(nazwa_ikony):
	ikona=pygame.Surface((32,32))
	ikona.set_colorkey((0,0,0))
	rawicon=pygame.image.load(nazwa_ikony)
	for i in range(0,32):
		for j in range(0,32):
			ikona.set_at((i,j), rawicon.get_at((i,j)))
	pygame.display.set_icon(ikona)
	
def wypisz_na_konsole():
	print 

#####################################################################

pygame.init()

wielkosc_ekranu=[szerokosc_ekranu,wysokosc_ekranu]
ekran=pygame.display.set_mode(wielkosc_ekranu)

pygame.display.set_caption("Strzelanka")
ustaw_ikone("ikona.bmp")

tlo=pygame.Surface(ekran.get_size())
tlo=tlo.convert()
tlo.fill(k_czarny)

pozycja_tla=[0,0]
zdjecie_tla=pygame.image.load("tlo.jpg").convert()

#####################################################################

w_ktora_strone_strzelac=0

font_1=pygame.font.Font(None, 25)
font_2=pygame.font.Font(None, 100)
wynik=0

czas_start_gry=0
czas_stop_gry=0

czas_start_naboje=0
czas_stop_naboje=0

czy_koniec_gry=0

czas_trwania_gry=15

wyswietlany_zegar=0

uzi=pygame.image.load("uzi.jpg").convert()
game_over=pygame.image.load("game_over.png").convert()

#####################################################################

class obiekt(pygame.sprite.Sprite):
	pozycja_x=0
	pozycja_y=0
	szerokosc=0
	wysokosc=0
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class sciana(obiekt):
	def __init__(self, wektor_polozenia, wektor_wielkosci, nazwa_pliku=""):
		pygame.sprite.Sprite.__init__(self)
		
		if nazwa_pliku!=str(""):
			self.image=pygame.image.load(nazwa_pliku)
		else:
			self.image=pygame.Surface(wektor_wielkosci)
			self.image.fill(k_niebieski)
		
		self.rect=self.image.get_rect()
		self.rect.left=wektor_polozenia[0]
		self.rect.top=wektor_polozenia[1]

class mob(obiekt):
	x=1
	y=1
	predkosc=[]
	
	def __init__(self, wektor_polozenia=[150,150], wektor_wielkosci=[30,30], predkosc=[1,1], nazwa_pliku=""):
		pygame.sprite.Sprite.__init__(self)
		
		if nazwa_pliku!=str(""):
			self.image=pygame.image.load(nazwa_pliku)
		else:
			self.image=pygame.Surface(wektor_wielkosci)
			self.image.fill(k_czerwony)
			
		self.rect=self.image.get_rect()
		self.rect.left=wektor_polozenia[0]
		self.rect.top=wektor_polozenia[1]
		
		self.predkosc=predkosc
		#self.predkosc[1]=predkosc[1]

	def zmien_predkosc(self, predkosc):
		self.x+=predkosc[0]
		self.y+=predkosc[1]

	def update(self, lista_obiektow_statycznych, lista_graczy):

		kolizja_gracze=pygame.sprite.spritecollide(self, lista_graczy, True)	#to jeszcze trzeba dopracowac poniewaz gracz znika z ekranu ale dalej mozna nim sterowac trzeba skasowac obiekt
		if kolizja_gracze:
			lista_graczy.remove()
			global czy_koniec_gry
			czy_koniec_gry=1
		
		stary_x=self.rect.left
		nowy_x=stary_x+self.x
		self.rect.left=nowy_x
			
		kolizja_statyczne=pygame.sprite.spritecollide(self, lista_obiektow_statycznych, False)
		if kolizja_statyczne:
			self.rect.left=stary_x
			if self.x>0:
				self.x=-self.predkosc[0]
			else:
				self.x=self.predkosc[0]
		
		stary_y=self.rect.top
		nowy_y=stary_y+self.y
		self.rect.top=nowy_y
		
		kolizja_statyczne=pygame.sprite.spritecollide(self, lista_obiektow_statycznych, False)
		if kolizja_statyczne:
			self.rect.top=stary_y		
			if self.y>0:
				self.y=-self.predkosc[1]
			else:
				self.y=self.predkosc[1]
		
class gracz(obiekt):
	x=0
	y=0
	
	def __init__(self, wektor_polozenia=[30,30], wektor_wielkosci=[20,20], liczba_amunicji=10, nazwa_pliku=""):
		pygame.sprite.Sprite.__init__(self)
		
		if nazwa_pliku!=str(""):
			self.image=pygame.image.load(nazwa_pliku)
		else:
			self.image=pygame.Surface(wektor_wielkosci)
			self.image.fill(k_niebieski)
		
		self.rect=self.image.get_rect()
		self.rect.left=wektor_polozenia[0]
		self.rect.top=wektor_polozenia[1]
		self.w_ktora_strone=1
		self.liczba_amunicji=liczba_amunicji
		
	def zmien_predkosc(self, x, y):
		if x>0:
			self.w_ktora_strone=1
		elif x<0:
			self.w_ktora_strone=0
			
		self.x+=x
		self.y+=y
		
	def update(self, lista_obiektow_statycznych):
		stary_x=self.rect.left
		nowy_x=stary_x+self.x
		self.rect.left=nowy_x

		kolizja=pygame.sprite.spritecollide(self, lista_obiektow_statycznych, False)
		if kolizja:
			self.rect.left=stary_x
		
		stary_y=self.rect.top
		nowy_y=stary_y+self.y
		self.rect.top=nowy_y
		
		kolizja=pygame.sprite.spritecollide(self, lista_obiektow_statycznych, False)
		if kolizja:
			self.rect.top=stary_y
			
		kolizja=pygame.sprite.spritecollide(self, lista_nabojow, True)
		if kolizja:
			lista_nabojow.remove()
			self.liczba_amunicji+=10
			
	def strzel(self):
		if self.liczba_amunicji>0:
			wektor_polozenia=[self.rect.left, self.rect.top]
			wektor_wielkosci=[8,4]
			pocisk_1=pocisk(wektor_polozenia, wektor_wielkosci, 20, self.w_ktora_strone, "pocisk.png")
		
			lista_pociskow_render.add(pocisk_1)
			self.liczba_amunicji-=1
	
	def zmniejsz_liczbe_amunicji(self):
		self.liczba_amunicji-=1
	
	def zwroc_liczbe_amunicji(self):
		return self.liczba_amunicji

class pocisk(obiekt):
	def __init__(self, wektor_polozenia, wektor_wielkosci, predkosc, w_ktora_strone, nazwa_pliku):	#przydaloby sie zrobic argumenty domniemane ale jest maly problem z strona strzelania
		pygame.sprite.Sprite.__init__(self)
		
		if nazwa_pliku!=str(""):
			self.image=pygame.image.load(nazwa_pliku)
		else:
			self.image=pygame.Surface(wektor_wielkosci)
			self.image.fill(k_zielony)
			
		if w_ktora_strone_strzelac==0:
			self.predkosc=predkosc
		else:
			self.predkosc=-predkosc
			
		self.wektor_polozenia=wektor_polozenia
		self.rect=self.image.get_rect()
		self.rect.left,self.rect.top=wektor_polozenia

	def update(self, lista_obiektow_statycznych):
		kolizja_statyczne=pygame.sprite.spritecollide(self, lista_obiektow_statycznych, False)
		kolizja_moby=pygame.sprite.spritecollide(self, lista_mobow, True)	
		
		if kolizja_statyczne or kolizja_moby:
			self.wektor_polozenia[0]+=800	#po tym dystansie pocisk zostanie usuniety
			self.rect.left,self.rect.top = [self.wektor_polozenia[0], self.wektor_polozenia[1]]
			if kolizja_moby:
				global wynik
				wynik+=1
			
		else:
			self.wektor_polozenia[0]=self.wektor_polozenia[0]+self.predkosc
			
			nowy_wektor_polozenia=[self.wektor_polozenia[0], self.wektor_polozenia[1]]
			self.rect.left,self.rect.top = nowy_wektor_polozenia	
		#ekran.blit(self.image, nowy_wektor_polozenia)		

class naboj(obiekt):
	def __init__(self, wektor_polozenia=[50,150], wektor_wielkosci=[10,10], nazwa_pliku=""):
		pygame.sprite.Sprite.__init__(self)
		
		if nazwa_pliku!=str(""):
			self.image=pygame.image.load(nazwa_pliku)
		else:
			self.image=pygame.Surface(wektor_wielkosci)
			self.image.fill(k_zielony)
			
		self.wektor_polozenia=wektor_polozenia
		self.rect=self.image.get_rect()
		self.rect.left,self.rect.top=wektor_polozenia

	#def update(self):	

#####################################################################

lista_obiektow_statycznych=pygame.sprite.RenderPlain()
sciana_1=sciana([0,0],[10,800],"sciana1.jpg")
lista_obiektow_statycznych.add(sciana_1)
sciana_1=sciana([0,590],[10,800],"sciana1.jpg")
lista_obiektow_statycznych.add(sciana_1)
sciana_1=sciana([0,10],[580,20],"sciana2.jpg")
lista_obiektow_statycznych.add(sciana_1)
sciana_1=sciana([780,10],[580,20],"sciana2.jpg")
lista_obiektow_statycznych.add(sciana_1)
sciana_1=sciana([390,10],[20,200])
lista_obiektow_statycznych.add(sciana_1)

#mob_1=mob([random.sample([100,150,200,250,300,350,700,750],1),random.sample([100,150,200,250,300,350,500,550],1)], [30,30], "mob1.png")
lista_mobow=pygame.sprite.RenderPlain()
mob_1=mob([random.randint(50,750), random.randint(50,550)], [30,30], [random.randint(1,4),random.randint(1,4)], "mob1.png")
lista_mobow.add(mob_1)
mob_1=mob([random.randint(50,750), random.randint(50,550)], [30,30], [random.randint(1,4),random.randint(1,4)], "mob1.png")
lista_mobow.add(mob_1)
mob_1=mob([random.randint(50,750), random.randint(50,550)], [30,30], [random.randint(1,4),random.randint(1,4)], "mob1.png")
lista_mobow.add(mob_1)
mob_1=mob([random.randint(50,750), random.randint(50,550)], [30,30], [random.randint(1,4),random.randint(1,4)], "mob1.png")
lista_mobow.add(mob_1)
mob_1=mob([random.randint(50,750), random.randint(50,550)], [30,30], [random.randint(1,4),random.randint(1,4)], "mob1.png")
lista_mobow.add(mob_1)
mob_1=mob([random.randint(50,750), random.randint(50,550)], [30,30], [random.randint(1,4),random.randint(1,4)], "mob1.png")
lista_mobow.add(mob_1)
mob_1=mob([random.randint(50,750), random.randint(50,550)], [30,30], [random.randint(1,4),random.randint(1,4)], "mob1.png")
lista_mobow.add(mob_1)

gracz_1=gracz([50,50],[10,10],30,"gracz1.png")
lista_graczy=pygame.sprite.RenderPlain()
lista_graczy.add(gracz_1)

lista_pociskow_render=pygame.sprite.RenderPlain()
lista_pociskow=[]	#stara lista ktora jest mi juz niepotrzebna

lista_nabojow=pygame.sprite.RenderPlain()

#####################################################################

clock=pygame.time.Clock()

czas_start_gry=time.time()
czas_start_naboje=time.time()
czy_zebrana_amunicja=0

koniec_glownej_petli=False

while koniec_glownej_petli==False:
	
	czas_stop_gry=time.time()
	
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			koniec_glownej_petli=True
		
		if czas_stop_gry-czas_start_gry<=czas_trwania_gry and czy_koniec_gry==0:
		
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					if w_ktora_strone_strzelac!=1:
						w_ktora_strone_strzelac=1			
					gracz_1.zmien_predkosc(-5,0)
				if event.key==pygame.K_RIGHT:
					if w_ktora_strone_strzelac!=0:
						w_ktora_strone_strzelac=0			
					gracz_1.zmien_predkosc(5,0)
				if event.key==pygame.K_UP:
					gracz_1.zmien_predkosc(0,-5)
				if event.key==pygame.K_DOWN:
					gracz_1.zmien_predkosc(0,5)
				
				if event.key==pygame.K_s:
					gracz_1.strzel()
					
			if event.type==pygame.KEYUP:
				if event.key==pygame.K_LEFT:
					gracz_1.zmien_predkosc(5,0)
				if event.key==pygame.K_RIGHT:
					gracz_1.zmien_predkosc(-5,0)
				if event.key==pygame.K_UP:
					gracz_1.zmien_predkosc(0,5)
				if event.key==pygame.K_DOWN:
					gracz_1.zmien_predkosc(0,-5)
					
		else:
			if czy_koniec_gry!=1:
				czy_koniec_gry=1
	
	if czy_koniec_gry!=1:
		gracz_1.update(lista_obiektow_statycznych)
	
	if len(lista_pociskow)>0:
		for pocisk_iterator in lista_pociskow:
			if pocisk_iterator.wektor_polozenia[0]>800 or  pocisk_iterator.wektor_polozenia[0]<0:
				lista_pociskow.remove(pocisk_iterator)
				pocisk_iterator.__del__(self)
			else:
				pocisk_iterator.update()
	
	if len(lista_pociskow_render)>0:
		for pocisk_iterator in lista_pociskow_render:
			if pocisk_iterator.wektor_polozenia[0]>800 or  pocisk_iterator.wektor_polozenia[0]<0:
				lista_pociskow_render.remove(pocisk_iterator)
			else:
				pocisk_iterator.update(lista_obiektow_statycznych)
				
	if len(lista_mobow)>0:
		for mob_iterator in lista_mobow:
			if mob_iterator.rect.left>800 or  mob_iterator.rect.top<0:
				lista_mobow.remove(mob_iterator)
			else:
				if czy_koniec_gry!=1:
					mob_iterator.update(lista_obiektow_statycznych, lista_graczy)
	
	if czas_stop_naboje-czas_start_naboje<=2.0:
		czas_stop_naboje=time.time()
	if czas_stop_naboje-czas_start_naboje>=2.0 and czas_stop_naboje-czas_start_naboje<=2.4:
		if czy_zebrana_amunicja==0:
			czy_zebrana_amunicja=1
			naboj_1=naboj([random.randint(50,750), random.randint(300,550)],[20,20])
			lista_nabojow.add(naboj_1)
	
	###draw###
	
	ekran.blit(zdjecie_tla, pozycja_tla)
	#ekran.fill(k_czarny)	#zamiast zdjecia

	lista_obiektow_statycznych.draw(ekran)
	lista_graczy.draw(ekran)
	lista_mobow.draw(ekran)
	lista_pociskow_render.draw(ekran)	

	ekran.blit(font_1.render("Your score: "+str(wynik),True,k_czarny), [20,10])
	
	if gracz_1.zwroc_liczbe_amunicji()==0:
		ekran.blit(font_1.render("Ammunition: "+str(gracz_1.zwroc_liczbe_amunicji()),True,k_czerwony), [460,10])
	else:
		ekran.blit(font_1.render("Ammunition: "+str(gracz_1.zwroc_liczbe_amunicji()),True,k_czarny), [460,10])
	
	if int(czas_trwania_gry-(czas_stop_gry-czas_start_gry))<=10 and czy_koniec_gry!=1:
		ekran.blit(font_1.render("Time to end: "+str(int(czas_trwania_gry-(czas_stop_gry-czas_start_gry))),True,k_czerwony), [620,10])
	else:
		if czy_koniec_gry!=1:
			ekran.blit(font_1.render("Time to end: "+str(int(czas_trwania_gry-(czas_stop_gry-czas_start_gry))),True,k_czarny), [620,10])
			#wyswietlany_zegar=int(czas_trwania_gry-(czas_stop_gry-czas_start_gry))
		#else:
			#ekran.blit(font_1.render("Time to end: "+str(wyswietlany_zegar),True,k_czarny), [620,10])
	
	lista_nabojow.draw(ekran)
	
	ekran.blit(uzi, [430,10])	

	if czy_koniec_gry==1:
		ekran.blit(font_2.render("GAME OVER",True,k_czarny), [200,230])
		ekran.blit(font_2.render("Your final score: "+str(wynik),True,k_czerwony), [140,300])
		ekran.blit(font_1.render("Press Q to quit game: ",True,k_czarny), [350,400])
	
	if event.type==pygame.KEYDOWN:
		if event.key==pygame.K_q:
			koniec_glownej_petli=True
	
	pygame.display.flip()
	
	clock.tick(30)

pygame.quit()
