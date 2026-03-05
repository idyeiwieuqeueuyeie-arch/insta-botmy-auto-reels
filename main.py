import os
import time
import random
import threading
from instagrapi import Client
from flask import Flask

# 1. إعداد السيرفر (عشان Render يقول Live)
app = Flask('')
@app.route('/')
def home(): return "<h1>Bot is Active!</h1>"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. إعدادات البوت
USER = "ug.31"
PASS = ".736alameri."
KEYWORDS = ["نصائح", "حكم", "عبارات"]
cl = Client()

# 3. وظيفة البوت (المحرك)
def start_bot():
    print("🚀 جاري بدء محرك البوت...")
    try:
        cl.login(USER, PASS)
        print("✅✅ تم تسجيل الدخول بنجاح!")
    except Exception as e:
        print(f"❌ فشل الدخول: {e}")
        return

    while True:
        try:
            tag = random.choice(KEYWORDS)
            print(f"🔍 جاري البحث في #{tag}...")
            medias = cl.hashtag_medias_top(tag, amount=5)
            for m in medias:
                if m.view_count > 500000 and m.media_type == 2:
                    print(f"🎥 تم العثور على ريلز (مشاهدات: {m.view_count})")
                    path = cl.video_download(m.pk, "./temp")
                    cl.video_upload(path, f"{m.caption_text}\n.\nتابعني للمزيد ❤️")
                    print("🎉 تم النشر بنجاح!")
                    if os.path.exists(path): os.remove(path)
                    time.sleep(14400) # انتظار 4 ساعات
                    break
            time.sleep(60)
        except Exception as e:
            print(f"⚠️ خطأ أثناء العمل: {e}")
            time.sleep(60)

# 4. نقطة الانطلاق (التشغيل الصحيح لـ Render)
if __name__ == "__main__":
    # تشغيل البوت في خيط (Thread) لكي لا يحبسه السيرفر
    t = threading.Thread(target=start_bot)
    t.start()
    
    # تشغيل السيرفر في المسار الرئيسي
    run_web()
    
