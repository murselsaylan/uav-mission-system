import json,random,time

def change_target_box(target_id):
    data = {"target_id": int(target_id)}
    
    with open('config/target.json', 'w') as file:
        json.dump(data, file)

def generate_connected_coordinates(num_points, width, height):
    """
    Bağlantılı koordinatlar üretir.
    
    Args:
        num_points (int): Üretilmesi gereken koordinat çifti sayısı.
        width (int): Maksimum genişlik.
        height (int): Maksimum yükseklik.
        
    Returns:
        list of dicts: Bağlantılı koordinatların listesi.
    """
    coordinates = []
    start_x, start_y = random.randint(0, width), random.randint(0, height)
    
    for _ in range(num_points):
        end_x, end_y = random.randint(0, width), random.randint(0, height)
        coordinates.append({"start": [start_x, start_y], "end": [end_x, end_y]})
        start_x, start_y = end_x, end_y  # Sonraki çizgi için bitiş noktasını yeni başlangıç yap

    return coordinates

def save_coordinates_to_json(coordinates, file_path):
    """
    Koordinatları bir JSON dosyasına kaydeder.
    
    Args:
        coordinates (list): Koordinat listesi.
        file_path (str): Kaydedilecek dosya yolu.
    """
    with open(file_path, 'w') as file:
        json.dump(coordinates, file, indent=4)
