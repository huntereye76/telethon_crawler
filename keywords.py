# =========================
# BASE KEYWORDS
# =========================
BASE_KEYWORDS = [

# =========================
# 💰 FINANCE / TRADING
# =========================
"trading", "trading signals", "intraday trading", "option trading",
"forex", "forex signals", "binary trading",
"crypto", "crypto signals", "bitcoin", "ethereum",
"nifty", "banknifty", "stock market", "share market",
"investment", "long term investment", "swing trading",
"commodity trading", "gold trading",

# =========================
# 💸 EARNING / BUSINESS
# =========================
"earn money", "online earning", "make money online",
"passive income", "work from home", "freelancing",
"affiliate marketing", "dropshipping", "reselling",
"startup", "business ideas", "side hustle",
"earn money india", "daily earning", "income ideas",

# =========================
# 💬 SOCIAL / FRIENDS
# =========================
"friends group", "friendship", "chat group",
"chatting group", "random chat", "stranger chat",
"indian chat group", "hindi chatting", "group chat",
"active group", "fun chat", "talk to strangers",

# =========================
# ❤️ DATING / RELATIONSHIP
# =========================
"dating group", "dating india", "single boys",
"single girls", "relationship talk",
"love chat", "couple chat", "flirting group",
"dating chat", "online dating", "real meet", "sex", "paid girls", "online bhabhi",

# =========================
# 😂 FUN / MEMES
# =========================
"memes", "funny memes", "viral memes",
"fun group", "entertainment group",
"comedy videos", "jokes group",
"funny videos", "timepass group",

# =========================
# 🎮 GAMING
# =========================
"gaming", "pubg", "bgmi", "free fire",
"call of duty", "gaming group",
"esports", "gaming community",
"minecraft", "gta", "valorant",

# =========================
# 📚 STUDY / EDUCATION
# =========================
"study group", "students group",
"jee preparation", "neet preparation",
"ssc exam", "upsc preparation",
"current affairs", "notes pdf",
"study material", "online classes",

# =========================
# 💻 TECH / PROGRAMMING
# =========================
"programming", "coding", "python",
"web development", "javascript",
"hacking", "ethical hacking",
"tech news", "ai tools", "machine learning",
"software development",

# =========================
# 📱 WHATSAPP / TELEGRAM
# =========================
"whatsapp group link", "telegram group link",
"join group", "join channel",
"public group", "active telegram group",
"new group link", "group invite link",

# =========================
# 🏏 SPORTS
# =========================
"cricket", "ipl", "football",
"kabaddi", "live match", "sports news",
"fantasy cricket", "dream11",
"match prediction",

# =========================
# 🎬 MOVIES / OTT
# =========================
"movies", "bollywood movies",
"hollywood movies", "web series",
"netflix series", "download movies",
"latest movies", "south movies",

# =========================
# 🛍️ SHOPPING / DEALS
# =========================
"amazon deals", "flipkart deals",
"discount offers", "loot deals",
"free recharge", "coupon codes",
"cashback offers",

# =========================
# 🧘 HEALTH / FITNESS
# =========================
"fitness", "gym workout",
"weight loss", "yoga",
"home workout", "diet plan",
"bodybuilding", "health tips",

# =========================
# 🌍 GENERAL / RANDOM
# =========================
"india", "global group",
"international chat", "community group",
"discussion group", "open group",
"public community"

] 

# =========================
# AUTO EXPANSION
# =========================
EXPANDED_KEYWORDS = []

for word in BASE_KEYWORDS:
    EXPANDED_KEYWORDS.extend([
        word,
        f"{word} group",
        f"{word} channel",
        f"{word} telegram",
        f"{word} india",
        f"{word} link",
        f"{word} join",
        f"{word} 2024",
        f"{word} 2025",
    ])

# =========================
# FINAL KEYWORDS
# =========================
KEYWORDS = list(set(EXPANDED_KEYWORDS))

