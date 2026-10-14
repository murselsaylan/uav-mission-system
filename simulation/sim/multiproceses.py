import subprocess
from multiprocessing import Process

def run_script(script_name):
    """Belirtilen Python script'ini çalıştırır."""
    subprocess.run(["python", script_name])

def main():
    # çalıştırlacak python isimlerini içeren tuple/list
    scripts = ("simv4.py", "hedeftakip.py")

    # Her script için bir süreç oluştur
    processes = [Process(target=run_script, args=(script,)) for script in scripts]

    # Süreçleri başlat
    for process in processes:
        process.start()

    # Tüm süreçlerin bitmesini bekle
    for process in processes:
        process.join()

if __name__ == "__main__":
    main()
