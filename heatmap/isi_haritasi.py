import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# Klasör yolları
images_folder = 'images'
labels_folder = 'labels'
output_folder = 'heatmaps'

# Çıktı klasörünü oluştur
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f" {output_folder} klasörü oluşturuldu")

# Tüm görsel dosyalarını bul
image_files = glob.glob(os.path.join(images_folder, '*.jpg'))

print(f" Toplam görsel dosyası: {len(image_files)}")
processed_count = 0

# Her görsel için ayrı ısı haritası oluştur
for image_path in image_files:
    # Dosya adından frame numarasını çıkar
    image_name = os.path.basename(image_path)
    frame_name = os.path.splitext(image_name)[0]  # uzantıyı kaldır
    
    # Karşılık gelen etiket dosyasını ara
    label_path = os.path.join(labels_folder, frame_name + '.txt')
    
    if os.path.exists(label_path) and os.path.getsize(label_path) > 0:
        try:
            # Görseli oku
            image = cv2.imread(image_path)
            if image is None:
                print(f" Görsel okunamadı: {image_path}")
                continue
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, _ = image.shape
            
            # Bu görsel için ısı haritası oluştur
            heatmap = np.zeros((h, w), dtype=np.float32)
            
            # Etiket dosyasını oku
            with open(label_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        cls, x, y, bw, bh = map(float, parts[:5])
                        
                        # YOLO formatından pixel koordinatlarına çevir
                        x1 = int((x - bw / 2) * w)
                        y1 = int((y - bh / 2) * h)
                        x2 = int((x + bw / 2) * w)
                        y2 = int((y + bh / 2) * h)
                        
                        # Sınırları kontrol et
                        x1 = max(0, min(x1, w-1))
                        y1 = max(0, min(y1, h-1))
                        x2 = max(0, min(x2, w))
                        y2 = max(0, min(y2, h))
                        
                        # Heatmap'e katkı ekle
                        if x2 > x1 and y2 > y1:
                            heatmap[y1:y2, x1:x2] += 1
            
            # Eğer tespit varsa işle
            if heatmap.max() > 0:
                # 🎨 Gaussian blur ve normalize
                heatmap_blurred = cv2.GaussianBlur(heatmap, (0, 0), sigmaX=20)
                heatmap_normalized = heatmap_blurred / heatmap_blurred.max()
                
                # 🖼 Görselleştirme
                plt.figure(figsize=(12, 6))
                
                # Sol taraf: Orijinal görsel
                plt.subplot(1, 2, 1)
                plt.imshow(image)
                plt.title(f"Orijinal Görsel\n{frame_name}")
                plt.axis('off')
                
                # Sağ taraf: Isı haritası
                plt.subplot(1, 2, 2)
                plt.imshow(image)
                plt.imshow(heatmap_normalized, cmap='jet', alpha=0.6)
                plt.title(f"Isı Haritası\n{int(heatmap.sum())} tespit")
                plt.axis('off')
                
                plt.tight_layout()
                
                # Kaydet
                output_path = os.path.join(output_folder, f"{frame_name}_heatmap.png")
                plt.savefig(output_path, dpi=150, bbox_inches='tight')
                plt.close()  # Belleği temizle
                
                processed_count += 1
                if processed_count % 10 == 0:
                    print(f" İşlenen: {processed_count}/{len(image_files)}")
                    
        except Exception as e:
            print(f"⚠️ Hata: {image_path} - {e}")

print(f"\nTamamlandı!")
print(f" Toplam işlenen dosya: {processed_count}")
print(f" Isı haritaları kaydedildi: {output_folder} klasöründe")
