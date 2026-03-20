import os
import re
import time
import random
import json
import psycopg2
from psycopg2.extras import execute_values
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.contacts import SearchRequest
from telethon.errors import FloodWaitError
from keywords import KEYWORDS

# ==============================
# CONFIG (TOGGLES)
# ==============================
SAVE_TO_FILE = True
SAVE_TO_DB = True

# ==============================
# LOAD ENV
# ==============================
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")
session_string = re.sub(r"\s+", "", session_string)
DB_URL = os.getenv("DB_URL")

# ==============================
# PROGRESS FILE
# ==============================
PROGRESS_FILE = "progress.json"

if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r") as f:
        progress = json.load(f)
        start_index = progress.get("index", 0)
else:
    start_index = 0

def save_progress(index):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"index": index}, f)

print(f"🔁 Resuming from index: {start_index}")

# ==============================
# FILE SETUP
# ==============================
OUTPUT_FILE = "tglink.txt"
existing_links = set()

if SAVE_TO_FILE:
    if not os.path.exists(OUTPUT_FILE):
        open(OUTPUT_FILE, "w").close()

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        existing_links = set(line.strip() for line in f if line.strip())

# ==============================
# DB CONNECT
# ==============================
if SAVE_TO_DB:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    print("✅ DB Connected")

# ==============================
# TELEGRAM CLIENT
# ==============================
client = TelegramClient(StringSession(session_string), api_id, api_hash)
client.start()

# ==============================
# SETTINGS
# ==============================
BATCH_SIZE = 50
MIN_DELAY = 2.5
MAX_DELAY = 5.5

batch_data = []

# ==============================
# MAIN LOOP
# ==============================
# while True:
for _ in range(1):  # run only one cycle

    print("\n🚀 New Cycle Started")

    # ⚠️ IMPORTANT: Don't shuffle if using progress
    # random.shuffle(KEYWORDS)

    for i in range(start_index, len(KEYWORDS)):
        keyword = KEYWORDS[i]
        print(f"\n🔍 [{i}] Searching: {keyword}")

        try:
            result = client(SearchRequest(q=keyword, limit=50))

            for chat in result.chats:
                username = getattr(chat, "username", None)

                if not username:
                    continue

                link = f"https://t.me/{username}"

                # ==============================
                # SAVE TO FILE
                # ==============================
                if SAVE_TO_FILE and link not in existing_links:
                    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                        f.write(link + "\n")

                    existing_links.add(link)
                    print("📁 Saved:", link)

                # ==============================
                # SAVE TO DB
                # ==============================
                if SAVE_TO_DB:
                    batch_data.append((link, f"search:{keyword}"))

                    if len(batch_data) >= BATCH_SIZE:
                        execute_values(
                            cur,
                            """
                            INSERT INTO crawl_queue (url, status, discovered_from)
                            VALUES %s
                            ON CONFLICT (url) DO NOTHING
                            """,
                            [(url, 'pending', src) for url, src in batch_data]
                        )
                        conn.commit()
                        print(f"🚀 Batch inserted {len(batch_data)}")
                        batch_data.clear()

        except FloodWaitError as e:
            print(f"⏳ FloodWait: sleeping {e.seconds}s")
            time.sleep(e.seconds)

        # ==============================
        # SAVE PROGRESS
        # ==============================
        save_progress(i)

        # ==============================
        # HUMAN DELAY
        # ==============================
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        print(f"😴 Sleeping {round(delay,2)} sec")
        time.sleep(delay)

    # ==============================
    # FINAL DB SAVE
    # ==============================
    if SAVE_TO_DB and batch_data:
        execute_values(
            cur,
            """
            INSERT INTO crawl_queue (url, status, discovered_from)
            VALUES %s
            ON CONFLICT (url) DO NOTHING
            """,
            [(url, 'pending', src) for url, src in batch_data]
        )
        conn.commit()
        print(f"🚀 Final batch inserted {len(batch_data)}")
        batch_data.clear()

    # ==============================
    # RESET PROGRESS AFTER FULL CYCLE
    # ==============================
    save_progress(0)
    start_index = 0

    # ==============================
    # AUTO REST
    # ==============================
    rest_time = random.randint(300, 900)
    print(f"\n🛑 Resting for {rest_time//60} minutes...")
    time.sleep(rest_time)
