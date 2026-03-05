import os
import time
import random
import threading
from instagrapi import Client
from datetime import datetime, timedelta
from flask import Flask

# --- 1. كود Flask (لإبقاء Render سعيداً) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Running Live!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. بيانات البوت ---
USER = "ug.31"
PASS = ".736alameri."
SEARCH_KEYWORDS = ["نصائح", "حكم", "عبارات"] 
FIXED_COMMENT = "تابعني للمزيد لطفا ❤️"

cl = Client()

# --- 3. وظيفة البوت الرئيسية ---
def run_bot():
    print("...جاري بدء محرك البوت")
    try:
        cl.login(USER, PASS)
        print("تم تسجيل الدخول بنجاح ✅")
    except Exception as e:
        print(f"خطأ في الدخول: {e}")
        return

    posted_today = 0
    while True:
        try:
            if posted_today < 3:
                tag = random.choice(SEARCH_KEYWORDS)
                print(f"جاري البحث في هاشتاج #{tag}...")
                
                medias = cl.hashtag_medias_top(tag, amount=7)
                for m in medias:
                    if m.view_count > 500000 and m.media_type == 2:
                        print(f"تم العثور على ريلز! مشاهداته: {m.view_count}")
                        path = cl.video_download(m.pk, "./temp")
                        final_caption = f"{m.caption_text}\n.\n{FIXED_COMMENT}"
                        
                        print("جاري الرفع الآن...")
                        cl.video_upload(path, final_caption)
                        
                        posted_today += 1
                        if os.path.exists(path): os.remove(path)
                        print(f"تم النشر بنجاح! العدد اليومي: {posted_today}")
                        time.sleep(14400) # انتظار 4 ساعات
                        break
            
            if datetime.now().hour == 0: posted_today = 0
            time.sleep(60)
        except Exception as e:
            print(f"خطأ أثناء العمل: {e}")
            time.sleep(60)

# --- 4. تشغيل المسارين معاً (المهم جداً) ---
if __name__ == "__main__":
    # تشغيل البوت في خيط (Thread) منفصل
    t = threading.Thread(target=run_bot)
    t.start()
    
    # تشغيل سيرفر الويب في المسار الرئيسي
    run_web_server()
    
    
  
