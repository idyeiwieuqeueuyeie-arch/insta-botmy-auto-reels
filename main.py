import os
import time
import random
import threading
from instagrapi import Client
from datetime import datetime
from flask import Flask

# 1. تشغيل السيرفر لإرضاء موقع Render
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. إعدادات البوت (تأكد من اليوزر والباسورد)
USER = "ug.31"
PASS = ".736alameri."
KEYWORDS = ["نصائح", "حكم", "عبارات"]

cl = Client()

# 3. محرك البوت (الذي سينفذ المهمة)
def start_bot():
    print("🚀 جاري محاولة الدخول...")
    try:
        cl.login(USER, PASS)
        print("✅ تم تسجيل الدخول بنجاح!")
    except Exception as e:
        print(f"❌ فشل الدخول: {e}")
        return

    while True:
        try:
            tag = random.choice(KEYWORDS)
            print(f"🔍 البحث في هاشتاج #{tag}")
            medias = cl.hashtag_medias_top(tag, amount=5)
            for m in medias:
                if m.view_count > 500000 and m.media_type == 2:
                    print(f"🎥 تم العثور على فيديو (مشاهدات: {m.view_count})")
                    path = cl.video_download(m.pk, "./temp")
                    cl.video_upload(path, f"{m.caption_text}\n.\nتابعني للمزيد ❤️")
                    if os.path.exists(path): os.remove(path)
                    print("🎉 تم النشر بنجاح!")
                    time.sleep(14400) # انتظار 4 ساعات
                    break
            time.sleep(60)
        except Exception as e:
            print(f"⚠️ خطأ: {e}")
            time.sleep(60)

# 4. تشغيل المسارين معاً (المسار الصحيح)
if __name__ == "__main__":
    # تشغيل السيرفر في خيط مستقل
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    
    # تشغيل البوت في المسار الرئيسي
    start_bot()
    
