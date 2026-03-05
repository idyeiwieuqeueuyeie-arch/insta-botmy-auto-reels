import os
import time
import random
import threading
from instagrapi import Client
from datetime import datetime
from flask import Flask

# 1. نظام الويب (لإرضاء Render ومنع التعليق)
app = Flask('')

@app.route('/')
def home():
    return "<h1>Bot is Active and Running!</h1>"

def run_flask():
    # Render يستخدم المنفذ 10000 غالباً
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. إعدادات الحساب
USER = "ug.31"
PASS = ".736alameri."
KEYWORDS = ["نصائح", "حكم", "عبارات"]

cl = Client()

# 3. محرك البوت (يعمل في الخلفية)
def start_bot_engine():
    print("🚀 جاري محاولة الدخول إلى إنستغرام...")
    try:
        cl.login(USER, PASS)
        print("✅ تم تسجيل الدخول بنجاح! البوت بدأ العمل الآن.")
    except Exception as e:
        print(f"❌ فشل الدخول: {e}")
        return

    posted_count = 0
    while True:
        try:
            if posted_count < 3:
                tag = random.choice(KEYWORDS)
                print(f"🔍 نبحث الآن في هاشتاج: #{tag}")
                
                medias = cl.hashtag_medias_top(tag, amount=5)
                for m in medias:
                    if m.view_count > 500000 and m.media_type == 2:
                        print(f"🎥 وجدنا فيديو لقطة! (مشاهدات: {m.view_count})")
                        path = cl.video_download(m.pk, "./temp")
                        
                        print("📤 جاري الرفع إلى حسابك...")
                        cl.video_upload(path, f"{m.caption_text}\n.\nتابعني للمزيد ❤️")
                        
                        posted_count += 1
                        if os.path.exists(path): os.remove(path)
                        print(f"🎉 تم النشر! إجمالي اليوم: {posted_count}")
                        
                        # انتظار 4 ساعات قبل النشر القادم
                        time.sleep(14400)
                        break
            
            # تصفير العداد في منتصف الليل
            if datetime.now().hour == 0:
                posted_count = 0
            
            time.sleep(60) # فحص كل دقيقة
        except Exception as e:
            print(f"⚠️ تنبيه: {e}")
            time.sleep(60)

# 4. نقطة الانطلاق (تشغيل المسارين معاً)
if __name__ == "__main__":
    # تشغيل البوت في "خيط" منفصل تماماً
    bot_thread = threading.Thread(target=start_bot_engine)
    bot_thread.daemon = True # يغلق مع إغلاق البرنامج
    bot_thread.start()
    
    # تشغيل السيرفر في المسار الرئيسي (هذا ما يراه Render)
    run_flask()
    
