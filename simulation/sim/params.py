import pygame
pygame.mixer.init()
# Ekran ayarları
screen_width = 1500
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
font_size = 20  # Font boyutu

# Renkler                            
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

#similasyon paremetreleri 
sayac = 1 
mission_failed = False  # Görevin başarısız olup olmadığını takip et
score = 0  # Skoru takip etmek için global bir değişken
fps = 15
mesaj_suresi = 4 *1000


#######################################################
#                içerik dosyları                      # 
#######################################################
hedefiha_png = pygame.image.load("config/hedefiha.png")
original_image_hedefiha = pygame.image.load("config/hedefiha.png").convert_alpha()  # Orijinal resmi yükle

iha_png = pygame.image.load("config/iha.png")
original_image_iha = pygame.image.load("config/iha.png").convert_alpha()  # Orijinal resmi yükle

airdefence_png = pygame.image.load("config/s400.png")

air_defence_sound = pygame.mixer.Sound("config/air_defence.wav")
targetlocked = pygame.mixer.Sound("config/targetlocked.wav")