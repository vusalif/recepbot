from instagrapi import Client
import json, os, time
import requests
import schedule

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

cl = Client()
cl.login(USERNAME, PASSWORD)

with open("frame_urls.json") as f:
    frames = json.load(f)

posted_index = 0
if os.path.exists("last_posted.txt"):
    with open("last_posted.txt") as f:
        posted_index = int(f.read())

def download_image(url, filename):
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)

def post_next():
    global posted_index
    if posted_index >= len(frames):
        print("✅ Done posting all frames.")
        return

    filename = f"temp.jpg"
    url = frames[posted_index]
    download_image(url, filename)

    caption = f"Recep İvedik 1 - #{posted_index + 1} out of {len(frames)}"
    cl.photo_upload(path=filename, caption=caption)

    posted_index += 1
    with open("last_posted.txt", "w") as f:
        f.write(str(posted_index))

    os.remove(filename)

# Post one now and schedule next every 15 min
post_next()
schedule.every(15).minutes.do(post_next)

while True:
    schedule.run_pending()
    time.sleep(10)
