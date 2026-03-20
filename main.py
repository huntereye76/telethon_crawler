import os
import time
import random
import psycopg2
from psycopg2.extras import execute_values
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.contacts import SearchRequest
from telethon.errors import FloodWaitError
from keywords import KEYWORDS

# ==============================
# LOAD FROM ENV (SECRETS)
# ==============================
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")
# FIX: remove unwanted line breaks
session_string = session_string.replace("\n", "").replace("\r", "").strip()
DB_URL = os.getenv("DB_URL")

print("Session length:", len(session_string))
print("Contains newline:", "\n" in session_string)

# ==============================
# FILE SETUP
# ==============================
OUTPUT_FILE = "tglink.txt"

if not os.path.exists(OUTPUT_FILE):
    open(OUTPUT_FILE, "w").close()

with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
    existing_links = set(line.strip() for line in f if line.strip())

# ==============================
# DB CONNECT
# ==============================
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()
print("✅ DB Connected")

# ==============================
# TELETHON CLIENT (STRING SESSION)
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
total_inserted = 0

# ==============================
# MAIN LOOP
# ==============================
while True:

    print("\n🚀 New Cycle Started")
    random.shuffle(KEYWORDS)

    for keyword in KEYWORDS:
        print(f"\n🔍 Searching: {keyword}")

        try:
            result = client(SearchRequest(q=keyword, limit=50))

            for chat in result.chats:
                username = getattr(chat, "username", None)

                if not username:
                    continue

                link = f"https://t.me/{username}"

                # ==============================
                # FILE SAVE
                # ==============================
                if link not in existing_links:
                    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                        f.write(link + "\n")

                    existing_links.add(link)
                    print("📁 Saved:", link)

                # ==============================
                # DB BATCH
                # ==============================
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
        # HUMAN DELAY
        # ==============================
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        print(f"😴 Sleeping {round(delay,2)} sec")
        time.sleep(delay)

    # ==============================
    # FINAL SAVE
    # ==============================
    if batch_data:
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
    # AUTO REST
    # ==============================
    rest_time = random.randint(300, 900)
    print(f"\n🛑 Resting for {rest_time//60} minutes...")
    time.sleep(rest_time)
