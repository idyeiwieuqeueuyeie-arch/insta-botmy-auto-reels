import os
import time
import random
import threading
from instagrapi import Client
from flask import Flask

# 1. السيرفر لإبقاء الخدمة تعمل
app = Flask('')
@app.route('/')
def home(): return "Bot is Active!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. بيانات الحساب
USER = "ug.31"
PASS = ".736alameri." # لو غيرت الباسورد حدثه هنا
KEYWORDS = ["نصائح", "حكم", "عبارات"]
cl = Client()

# 3. وظيفة البوت مع حماية (نظام السامسونج)
def start_bot():
    print("🚀 جاري الانتظار قليلاً قبل الدخول للأمان...")
    time.sleep(random.randint(30, 60)) # انتظار عشوائي
    
    try:
        # إيهام إنستغرام بأنك تستخدم جوال حقيقي
        cl.set_device_settings({
            "app_version": "269.0.0.18.75",
            "android_version": 26,
            "android_release": "8.0.0",
            "dpi": "480dpi",
            "resolution": "1080x1920",
            "manufacturer": "Samsung",
            "device_model": "SM-G950F",
        })
        cl.login(USER, PASS)
        print("✅✅ تم تسجيل الدخول بنجاح!")
    except Exception as e:
        print(f"❌ فشل الدخول: {e}")
        return

    while True:
        try:
            tag = random.choice(KEYWORDS)
            print(f"🔍 البحث عن ريلز في #{tag}...")
            medias = cl.hashtag_medias_top(tag, amount=5)
            for m in medias:
                if m.view_count > 500000 and m.media_type == 2:
                    print(f"🎥 تم العثور على ريلز لقطة! (مشاهدات: {m.view_count})")
                    path = cl.video_download(m.pk, "./temp")
                    cl.video_upload(path, f"{m.caption_text}\n.\nتابعني للمزيد ❤️")
                    print("🎉 تم النشر بنجاح!")
                    if os.path.exists(path): os.remove(path)
                    time.sleep(14400) # انتظار 4 ساعات
                    break
            time.sleep(120) # انتظار بين عمليات البحث
        except Exception as e:
            print(f"⚠️ تنبيه: {e}")
            time.sleep(300)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    start_bot()
    
