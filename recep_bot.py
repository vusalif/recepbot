import os
import time
import schedule
from instabot import Bot

# Login from environment variables
USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


bot = Bot()
bot.login(username=USERNAME, password=PASSWORD)

FOLDER = "all_frames"
POST_LOG = "last_posted.txt"
TOTAL_FRAMES = 3050  # total number of frames

# Load index
posted = 0
if os.path.exists(POST_LOG):
    with open(POST_LOG) as f:
        posted = int(f.read())

frames = sorted(os.listdir(FOLDER))

def post_next():
    global posted
    if posted >= len(frames):
        print("✅ All frames posted.")
        return

    frame = frames[posted]
    path = os.path.join(FOLDER, frame)
    print(f"📸 Posting {path}...")

    caption = f"Recep İvedik 1 – Frame #{posted + 1} out of {TOTAL_FRAMES}"

    bot.upload_photo(path, caption=caption)
    posted += 1

    with open(POST_LOG, "w") as f:
        f.write(str(posted))

schedule.every(15).minutes.do(post_next)
post_next()  # post one instantly

while True:
    schedule.run_pending()
    time.sleep(10)
