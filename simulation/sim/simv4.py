import pygame,random,math,json
from params import * 
from simclass import *
from threading import Thread
from pygame.font import Font
from hedeftakip import follow_target

# Pygame başlatılıyor
pygame.init()
pygame.font.init()
pygame.mixer.init()



def logger(inf_list):
    if sayac % fps == 0:
        with open('config/ihas.json', 'w') as f:
            json.dump(inf_list, f)   

    
         
# Oyun döngüsü
while running:
    
######## değişken işlemleri ############################

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    delta_time = clock.tick(45) / 1000  # Delta zamanı saniye cinsinden hesapla
    total_inside_time = 0  # Hava savunma sistemlerinin toplam iç süresi
    sayac +=1
    inf_list =[]
    screen.fill(BLACK)
    draw_info_panel(score)

#****************************************************#
# Hedef İHA'yı seçme
    hedef_iha_id = "Hedef_iha_3"
    with open('config/ihas.json', 'r') as f:
        ihas_data = json.load(f)
    
    selected_iha = None
    for iha_data in ihas_data:
        if iha_data["id"] == hedef_iha_id:
            selected_iha = iha_data
            break

    if selected_iha is not None:
        follow_target(iha, selected_iha)
    else:
        print("Hedef İHA bulunamadı!")

#****************************************************#



######## similasyon içeriği ############################


    for hava_savunma in all_sprites:
        if isinstance(hava_savunma,KamikazeHedefi):
            data = {"id": hava_savunma.name, "x": hava_savunma.rect.centerx, "y": hava_savunma.rect.centery}
            inf_list.append(data)
        if isinstance(hava_savunma, HavaSavunmaSistemi):
            data = {"id": hava_savunma.name, "x": hava_savunma.rect.centerx, "y": hava_savunma.rect.centery,"cap":hava_savunma.radius}
            inf_list.append(data)
            inside = is_drone_inside_defense(iha.rect.centerx, iha.rect.centery, hava_savunma.rect.centerx, hava_savunma.rect.centery, hava_savunma.radius)
            if inside:
                hava_savunma.change_color(ORANGE)
                hava_savunma.inside_timer += delta_time  # Sadece İHA içerideyken süreyi güncelle
                if not hava_savunma.active:
                    air_defence_sound.play()
                    hava_savunma.active = True
            else:
                hava_savunma.change_color(GREEN)
                
                if hava_savunma.active and hava_savunma.color == GREEN:
                    air_defence_sound.stop()
                    hava_savunma.active = False

               
            total_inside_time += hava_savunma.inside_timer  # Toplam süreyi hesapla
            
    for hedef_iha in hedef_ihas:
        data = {"id": hedef_iha.name, "x": hedef_iha.rect.centerx, "y": hedef_iha.rect.centery, "speed": hedef_iha.speed, "direction": hedef_iha.direction *(180/3.14)} 
        inf_list.append(data)
        distance = math.sqrt((iha.rect.centerx - hedef_iha.rect.centerx) ** 2 + (iha.rect.centery - hedef_iha.rect.centery) ** 2)
        # Takip ediliyorsa, hedefin etrafına yeşil bir kutu çiz
        if distance < 80:
            
            hedef_iha.update_close_timer(delta_time)
            pygame.draw.rect(screen, GREEN, hedef_iha.rect.inflate(20, 20), 2)  # Hedefin etrafında 20 piksel genişliğinde bir yeşil kutu çiz
            
            if hedef_iha.close_timer >= 4 :
                score += 1
                targetlocked.play()
                hedef_iha.reset_close_timer()  # Skoru artırdıktan sonra zamanlayıcıyı sıfırla
        else:
            hedef_iha.reset_close_timer()
        if hedef_iha.id == hedef_iha.target_id:       
            draw_dashed_rect(screen, pygame.Color('red'), hedef_iha.rect)    
    data = {"id": iha.name, "x": iha.rect.centerx, "y": iha.rect.centery, "speed": iha.speed, "direction": iha.direction}
    inf_list.append(data)
      
    # JSON dosyası
    logger(inf_list) # nesnelerin bilgilerini gönder
    rota_ciz(screen, koordinat_Al(), color=(255, 0, 0))  # Koordinatlara göre çizgileri çiz
    # Görev başarısızsa, toplam iç süre 20 saniyeyi geçerse, oyunu sonlandır
    
    if total_inside_time >= 20:
        font = pygame.font.SysFont(None, 180)
        text = font.render('Görev Başarısız', True, RED)
        screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2))
        running = False
        
              
#****************************************************# 
    
    all_sprites.update()    
    all_sprites.draw(screen)  
    pygame.display.flip()
    
pygame.time.wait(mesaj_suresi)  # Mesajı göster
pygame.quit()