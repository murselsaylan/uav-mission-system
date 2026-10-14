import math
from params import *
from simclass import *
import win32api
import win32con


def follow_target(iha, selected_iha):
    # İHA'nın konumu ve hedef İHA'nın konumu
    iha_x, iha_y = iha.rect.centerx, iha.rect.centery
    hedef_x, hedef_y = selected_iha["x"], selected_iha["y"]

    dx = hedef_x - iha_x
    dy = hedef_y - iha_y

    angle = calculate_angle(dx, dy)

    if iha.direction != angle:
        turn_rate = iha.turn_rate
    
        if (angle - iha.direction) % 360 > 180:
            iha.direction = (iha.direction - turn_rate) % 360
        else:
            iha.direction = (iha.direction + turn_rate) % 360

    distance_to_target = ((dx ** 2) + (dy ** 2)) ** 0.5

    # Hedefe olan uzaklık azaldıkça İHA'nın hızını azalt
    max_speed = 6  # Maksimum hız
    min_speed = 3  # Minimum hız
    max_distance = 30  # İHA'nın maksimum hızını kullanmaya başlayacağı mesafe
    min_distance =50   # İHA'nın minimum hızını kullanmaya başlayacağı mesafe
    speed_rate = 0.1    # Hız azaltma ve artırma oranı

    if distance_to_target < min_distance:
        if iha.speed > min_speed:
            # "W" tuşuna basılmış gibi davran
            win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        else:
            # "W" tuşunu bırak
            win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif distance_to_target > max_distance:
        if iha.speed < max_speed:
            # "S" tuşuna basılmış gibi davran
            win32api.keybd_event(0x53, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        else:
            # "S" tuşunu bırak
            win32api.keybd_event(0x53, 0, win32con.KEYEVENTF_KEYUP, 0)
    else:
        # Tuşları bırak
        win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x53, 0, win32con.KEYEVENTF_KEYUP, 0)


   


def calculate_angle(dx, dy):
    # Payda sıfır olma durumunu kontrol et
    if dx == 0:
        # Eğer dx sıfırsa, dikdörtgenin kenarına yaklaşıyoruz, bu durumda özel bir durum var
        if dy > 0:
            return 90  # İHA, hedefin üzerinde olduğunda 90 derece açıya sahiptir
        elif dy < 0:
            return 270  # İHA, hedefin altında olduğunda 270 derece açıya sahiptir
        else:
            return 0  # dx ve dy sıfırsa, açı tanımsızdır, bu nedenle İHA sabit bir yöne sahiptir
    else:
       
        angle = math.atan(dy / dx)
        
        
        if dx > 0 and dy >= 0:
            # 1. çeyrek
            return math.degrees(angle)
        elif dx < 0:
            # 2. veya 3. çeyrek
            return 180 + math.degrees(angle)
        else:
            # 4. çeyrek
            return 360 + math.degrees(angle)