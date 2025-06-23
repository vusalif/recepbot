from instagrapi import Client
import os
import time
import requests
import schedule
from PIL import Image

cl = Client()

# Əvvəlcə session varsa, istifadə et
if os.path.exists("session.json"):
    cl.load_settings("session.json")
    try:
        cl.get_timeline_feed()  # Sadə yoxlama, session keçərlidirmi
        print("✅ Session işləyir.")
    except:
        print("⚠️ Session keçərsizdir, yenidən login olunur.")
        cl.login("recepivedikframe", "1905Fatihterim")
        cl.dump_settings("session.json")
else:
    cl.login("recepivedikframe", "1905Fatihterim")
    cl.dump_settings("session.json")

# Linkləri fayldan oxuyuruq
with open("drive_links.txt") as f:
    frames = [line.strip() for line in f if line.strip()]

# Hansı frame-dən başlayırıq, onu saxlayır
posted_index = 0
if os.path.exists("last_posted.txt"):
    with open("last_posted.txt") as f:
        posted_index = int(f.read())

# Şəkil hazırlama funksiyası (Instagram üçün uyğunlaşdırırıq)
def prepare_image(filename):
    img = Image.open(filename)
    img = img.convert("RGB")  # Rəng formatını düzəldir
    img.save(filename, "JPEG")

# Şəkil endir və paylaş
def post_next():
    global posted_index
    if posted_index >= len(frames):
        print("✅ Bütün frame-lər paylaşılıb.")
        return

    filename = "temp.jpg"
    url = frames[posted_index]
    download_image(url, filename)

    prepare_image(filename)  # Instagram üçün şəkli hazırlayırıq

    caption = f"Recep İvedik 1 - #{posted_index + 1} out of {len(frames)} / #recepivedik"

    try:
        cl.photo_upload(path=filename, caption=caption)
        print(f"✅ Paylaşıldı: {caption}")
    except Exception as e:
        print(f"⚠️ Paylaşım zamanı xəta baş verdi: {e}")

    posted_index += 1
    with open("last_posted.txt", "w") as f:
        f.write(str(posted_index))

    if os.path.exists(filename):
        os.remove(filename)

# Şəkil endirən funksiya
def download_image(url, filename):
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)

# İlk paylaşım və schedule qururuq
post_next()
schedule.every(5).minutes.do(post_next)

while True:
    schedule.run_pending()
    time.sleep(10)
