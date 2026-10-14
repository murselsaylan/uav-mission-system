import pygame,random,math,sys,time ,json,os
from params import *
from pygame.font import Font

pygame.font.init()



# Oyun döngüsü kontrolü
running = True
clock = pygame.time.Clock()
    
# Sprite grupları
all_sprites = pygame.sprite.Group()
hedef_ihas = pygame.sprite.Group()


#######################################################
#                fonksiyonlar                         # 
#######################################################

def calculate_radius(area_coverage, num_circles):
    # Toplam kapsama alanını hesaplayarak her bir dairenin yarıçapını bulur
    total_area = screen_width * screen_height
    circle_area = (total_area * area_coverage) / num_circles
    radius = math.sqrt(circle_area / math.pi)
    return int(radius)

def draw_info_panel(score):
    # Panel alanını çiz
    panel_rect = pygame.Rect(0, screen_height , screen_width, 0)
    pygame.draw.rect(screen, BLACK, panel_rect)

    # Sayaç bilgisini ve diğer metinleri burada gösterebilirsiniz
    font = pygame.font.SysFont(None, font_size)
    for index, hava_savunma in enumerate(all_sprites):
        if isinstance(hava_savunma, HavaSavunmaSistemi):
            text = font.render(f'Hava Savunma {hava_savunma.id}: {hava_savunma.inside_timer:.2f} s', True, WHITE)
            screen.blit(text, (10, screen_height -90 + 30*index))
    
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Skor: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))        
    
def is_drone_inside_defense(drone_x, drone_y, defense_x, defense_y, radius):
    distance = math.sqrt((drone_x - defense_x) ** 2 + (drone_y - defense_y) ** 2)
    return distance < radius

def draw_dashed_rect(surface, color, rect, dash_length=10):
    """
    Bir yüzey üzerinde belirtilen bir dikdörtgenin etrafına kesikli çizgiler çizer.
    surface: Çizimin yapılacağı Pygame yüzeyi.
    color: Çizgi rengi.
    rect: Pygame Rect nesnesi, çizimin yapılacağı dikdörtgen.
    dash_length: Kesiklerin uzunluğu.
    """
    x1, y1, w, h = rect  # Dikdörtgenin koordinatları ve boyutları
    x2, y2 = x1 + w, y1 + h

    # Üst ve alt çizgiler
    for x in range(x1, x2, dash_length * 2):
        end = min(x + dash_length, x2)
        pygame.draw.line(surface, color, (x, y1), (end, y1))
        pygame.draw.line(surface, color, (x, y2), (end, y2))

    # Sol ve sağ çizgiler
    for y in range(y1, y2, dash_length * 2):
        end = min(y + dash_length, y2)
        pygame.draw.line(surface, color, (x1, y), (x1, end))
        pygame.draw.line(surface, color, (x2, y), (x2, end))
        
def koordinat_Al():
    file_path = 'config/koordinat.json'
    # Dosyanın varlığını ve boş olup olmadığını kontrol et
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print("Dosya bulunamadı veya boş.")
        return []  # Boş bir liste dönerek hata durumunu ele al

    with open(file_path, 'r') as file:
        try:
            coordinates = json.load(file)
            return coordinates
        except json.JSONDecodeError:
            print("JSON dosyası okunurken bir hata oluştu.")
            return []  # JSON okuma hatası durumunda boş liste dön

def rota_ciz(surface, coordinates, color=(255, 255, 255), dash_length=5):
    """
    Koordinat listesine göre yüzeye çizgiler çizer.
    """
    for coord in coordinates:
        start_pos = tuple(coord["start"])
        end_pos = tuple(coord["end"])
        draw_dashed_line(surface, color, start_pos, end_pos, dash_length)

def draw_dashed_line(surface, color, start_pos, end_pos, dash_length=10):
    """
    Bir yüzey üzerinde başlangıç ve bitiş koordinatları arasında kesikli bir çizgi çizer.
    
    Args:
        surface: Çizimin yapılacağı Pygame yüzeyi.
        color: Çizginin rengi.
        start_pos (tuple): Çizginin başlangıç koordinatı (x, y).
        end_pos (tuple): Çizginin bitiş koordinatı (x, y).
        dash_length (int): Her bir kesik parçanın uzunluğu.
    """
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    distance = max(abs(dx), abs(dy))
    for i in range(0, distance, dash_length * 2):
        segment_start = (x1 + dx * (i/distance), y1 + dy * (i/distance))
        segment_end = (x1 + dx * ((i + dash_length)/distance), y1 + dy * ((i + dash_length)/distance))
        pygame.draw.line(surface, color, segment_start, segment_end)

#######################################################
#                sınıflar                             # 
#######################################################

class Entity(pygame.sprite.Sprite):
    def __init__(self,color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - width)
        self.rect.y = random.randint(0, screen_height - height)
 

    def update(self):
        pass

class IHA(Entity):
    def __init__(self, id):
        super().__init__(BLUE, 10, 10)
        self.id = id
        self.name = "ilgeru"
        self.speed = 0  # Başlangıç hızı
        self.speed_rate = 0.2 # ivmelendirme + -
        self.direction = 0  # Başlangıç yönü (derece cinsinden)
        self.turn_rate = 3  # Her tuş basımında dönüş miktarı (derece)
        
        # Resmi ve konumunu ayarla
        self.original_image = iha_png
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        
    def update(self):
        keys = pygame.key.get_pressed()

        # Hız kontrolü
        if keys[pygame.K_w] and self.speed <= 5:
            self.speed = self.speed + self.speed_rate
        if keys[pygame.K_s] and self.speed >= 2:
            self.speed = self.speed - self.speed_rate

        # Dönüş kontrolü
        if keys[pygame.K_a]:
            self.direction = (self.direction - self.turn_rate) % 360
        if keys[pygame.K_d]:
            self.direction = (self.direction + self.turn_rate) % 360
        
        # Yeni konumu hesapla
        radian_angle = math.radians(self.direction)
        new_x = self.rect.x + int(self.speed * math.cos(radian_angle))
        new_y = self.rect.y + int(self.speed * math.sin(radian_angle))
        
        # Ekran sınırları içinde kalmasını sağla
        if 0 <= new_x <= screen_width - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= screen_height - self.rect.height:
            self.rect.y = new_y
        # Resmi döndür
        self.rotate_image()

    def rotate_image(self):
        """Resmi, mevcut yönüne göre döndürür ve merkezini korur."""
        current_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, -self.direction)
        self.rect = self.image.get_rect(center=current_center)
 
class HedefIHA(Entity):
    def __init__(self, id):
        super().__init__(BLACK, 10, 10)
        self.id = id
        self.name = "Hedef_iha_" + str(id)
        self.speed = random.randint(1,3)
        self.acceleration = 0.1  # Hızlanma oranı
        self.target_speed = self.speed  # Hedef hız
        self.direction = random.uniform(0, 2 * math.pi)  # Radyan cinsinden yön
        self.target_direction = self.direction  # Hedef yön
        self.turn_rate = math.radians(random.uniform(2,4))  # Radyan cinsinden dönüş oranı
        self.close_timer = 0
        self.nspeed = 0
        self.center_x = screen_width / 2
        self.center_y = screen_height / 2
        self.last_update_time = time.time()
        self.update_interval = 0.2  # Yeni hız ve yön belirlemek için aralık (saniye)
        self.target_id = None
        
        # Resim ve konum ayarları
        self.image = original_image_hedefiha
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        self.rect = self.image.get_rect(center=(x, y))


                   
    def update(self):
        # Hedef hıza doğru hızlanma veya yavaşlama
        self.newspeed()
        # Yavaş yavaş hedef yönüne dön
        self.newdirection()
        
        # Yeni konumu hesapla
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        # Ekranın sınırlarına yaklaştığında hedef yönü ekranın merkezine çevir
        buffer = 150  # Sınır tanımlama buffer'ı
        if (self.rect.left < buffer or self.rect.right > screen_width - buffer or 
            self.rect.top < buffer or self.rect.bottom > screen_height - buffer):
            # Ekranın merkezine doğru yeni bir hedef yön hesapla
            self.target_direction = math.atan2(self.center_y - self.rect.centery, 
                                               self.center_x - self.rect.centerx)
   
        # Yeni konumu hesapla
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))
        
        font = pygame.font.SysFont("Arial", font_size)
        id_text = font.render(str(self.id), True, (255, 255, 255))  # Beyaz renk
        screen.blit(id_text, (self.rect.x + 5, self.rect.y - font_size)) 
        # Resmi döndür
        self.rotate_image()
        target = self.load_information()
        self.target_id = target["target_id"]
    
    
    def load_information(self):
        default_value = {"target_id": 300}
        file_path="config/target.json"
        # Dosyanın varlığını kontrol et
        if not os.path.exists(file_path):
            return default_value

        # Dosyanın boş olup olmadığını kontrol et
        if os.path.getsize(file_path) == 0:
            return default_value

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
            
        except json.JSONDecodeError as e:
            return default_value

    def newspeed(self):
        # Hedef hızı belirle
        if 1.5 < self.speed < 3:
            # Hızın artırılması veya azaltılması için rastgele bir işaret (+1 veya -1) seç
            sign = random.choice([1, -1])
            # Hız değişikliğini hesapla
            speed_change = sign * random.randint(1, 2) * self.acceleration
            # Hedef hızı hesapla
            target_speed = self.speed + speed_change
        else:
            target_speed = 2

        # Mevcut hızı hedef hıza doğru güncelle
        if self.speed < target_speed:
            self.speed = min(self.speed + self.acceleration, target_speed)
        elif self.speed > target_speed:
            self.speed = max(self.speed - self.acceleration, target_speed)
    
    def newdirection(self):
        # Hedef yönü belirle (Örneğin, tamamen rastgele bir yön)
        if random.randint(0, 60) == 0:  # Belirli bir oranda yeni bir hedef yön belirle
            self.target_direction = random.uniform(0, 2 * math.pi)
        
        # Mevcut yön ile hedef yön arasındaki fark
        direction_difference = self.target_direction - self.direction
        # Farkı [-pi, pi] aralığına sınırla
        direction_difference = (direction_difference + math.pi) % (2 * math.pi) - math.pi

        # Yön farkına göre mevcut yönü ayarla
        if abs(direction_difference) > self.turn_rate:
            self.direction += self.turn_rate if direction_difference > 0 else -self.turn_rate
        else:
            self.direction = self.target_direction

        # Yönü [0, 2*pi] aralığında tut
        self.direction %= 2 * math.pi

    def rotate_image(self):
        """Resmi, mevcut yönüne göre döndürür ve merkezini korur."""
        current_center = self.rect.center
        angle = math.degrees(-self.direction) + 90
        self.image = pygame.transform.rotate(original_image_hedefiha, angle)
        self.rect = self.image.get_rect(center=current_center)
    
    def reset_close_timer(self):
        self.close_timer = 0

    def update_close_timer(self, delta_time):
        self.close_timer += delta_time    

class HavaSavunmaSistemi(Entity):
    def __init__(self,id):
        self.radius = calculate_radius(random.uniform(0.10, 0.20), 4)
        self.color = GREEN  # Başlangıç rengi olarak yeşil
        self.inside_timer = 0  # İHA'nın içinde geçirdiği süreyi saniye cinsinden takip etmek için
        self.id = id 
        self.name = "hava_savunma_" + str(id)
        super().__init__(self.color, self.radius*2, self.radius*2)
        self.update_image()
        self.active = False       

    def update_image(self):
        self.image = pygame.Surface([self.radius*2, self.radius*2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        font = pygame.font.SysFont("Arial", font_size)
        id_text = font.render(str(self.id), True, (255, 255, 255))  # Beyaz renk
        screen.blit(id_text, (self.rect.x + 5, self.rect.y - font_size)) 
        resim = pygame.image.load('config/s400.png').convert_alpha()
        # Resmi, çemberin üstüne, merkezi ayarlayarak blit et
        resim_rect = resim.get_rect(center=(self.radius, self.radius))
        self.image.blit(resim, resim_rect)
                
    def change_color(self, new_color):
        self.color = new_color
        self.update_image()
   
    # Timer'ı güncelle
    def update_timer(self, delta_time):
        self.inside_timer += delta_time
        
        if self.inside_timer >= 20:  # 20 saniyeyi kontrol et
            return True
        return False
    
    def create_hava_savunma_system(id, screen_width, screen_height):
        border =150
        min_distance = 200  # Hava savunma sistemleri arasındaki minimum mesafe
        max_attempts = 100  # Uygun konum bulma denemelerinin maksimum sayısı
        for attempt in range(max_attempts):
            # Rastgele bir konum seç
            x = random.randint(border, screen_width - border)
            y = random.randint(border, screen_height - border)
            new_system = HavaSavunmaSistemi(id)
            new_system.rect.center = (x, y)
            
            # Mevcut sistemlerle arasındaki mesafeyi kontrol et
            too_close = any(math.hypot(system.rect.centerx - x, system.rect.centery - y) < min_distance for system in existing_defense_systems)
            
            if not too_close:
                existing_defense_systems.append(new_system)
                return new_system
        return None  # Uygun bir konum bulunamazsa None döndür
    
class KamikazeHedefi(Entity):
    def __init__(self,id):
        super().__init__(WHITE, 20, 20)
        self.id = id
        self.name = "kamikaze"
        
#######################################################
#                Nesneler                             # 
#######################################################
existing_defense_systems = []      
# Nesneler oluşturuluyor
for i in range(3):
    hava_savunma = HavaSavunmaSistemi.create_hava_savunma_system(i, screen_width, screen_height)
    if hava_savunma is not None:
        all_sprites.add(hava_savunma)

kamikaze_hedefi = KamikazeHedefi(1)
all_sprites.add(kamikaze_hedefi)

for _ in range(10):
    hedef_iha = HedefIHA(_)
    all_sprites.add(hedef_iha)
    hedef_ihas.add(hedef_iha)

iha = IHA(255)
all_sprites.add(iha)        
        