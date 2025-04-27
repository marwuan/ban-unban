import requests
import time
from telebot import TeleBot

# بيانات التليجرام
TOKEN = '7222767045:AAEKkLPQFMiC_ozmgDH3u9CjMkQC9DtgzAk'
CHAT_ID = '7632067840'

# أسماء الحسابات المراد مراقبتها
usernames = [
    'jpux',
    'ypux'
]

# هيدرات كاملة تحاكي متصفح
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://www.instagram.com/"
}

# تحميل البروكسيات من ملف
def load_proxies():
    with open('proxies.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]

proxies_list = load_proxies()

# تهيئة البوت
bot = TeleBot(TOKEN)

# رابط الحسابات
urls = {username: f"https://www.instagram.com/{username}/" for username in usernames}

# حالات الحسابات
status = {username: False for username in usernames}

import random

while True:
    for username, url in urls.items():
        success = False
        attempts = 0
        
        # Add random delay between requests (5-15 seconds)
        delay = random.uniform(5, 15)
        time.sleep(delay)

        while not success and attempts < 3:  # Reduced max attempts to 3
            if not proxies_list:
                print("ماكو بروكسيات متوفرة.")
                break

            proxy = random.choice(proxies_list)
            proxies = {
                'http': proxy,
                'https': proxy
            }

            try:
                response = requests.get(url, headers=headers, proxies=proxies, timeout=10)

                if response.status_code == 200:
                    if status[username]:
                        bot.send_message(CHAT_ID, f"رجع حساب {username} يشتغل! \n\nنورت الانستا يا وردة!")
                        status[username] = False
                    success = True
                elif response.status_code == 404:
                    if not status[username]:
                        bot.send_message(CHAT_ID, f"الحساب {username} اختفى أو تعطل!")
                        status[username] = True
                    success = True
                elif response.status_code == 429:
                    wait_time = 60  # Wait 1 minute when rate limited
                    bot.send_message(CHAT_ID, f"⚠️ تحذير: تم تجاوز حد الطلبات. سننتظر {wait_time} ثانية قبل المحاولة مرة أخرى.\nالحساب: {username}")
                    time.sleep(wait_time)
                    proxies_list.remove(proxy)  # Remove rate-limited proxy
                    if not proxies_list:
                        proxies_list = load_proxies()  # Reload proxies if empty
                    continue
                else:
                    print(f"استجابة غير متوقعة للحساب {username}: {response.status_code}")
                    success = True

            except Exception as e:
                print(f"فشل الاتصال بالبروكسي {proxy}. رح نحاول ببروكسي ثاني...")
                attempts += 1

        if not success:
            # اذا خلصت المحاولات كلها وفشل
            bot.send_message(CHAT_ID, f"❗️ فشل التحقق من حساب {username} لأن كل البروكسيات ماتت أو ما استجابت.")

    time.sleep(60)  # بعد ما يكمل جميع الحسابات ينتظر دقيقة
