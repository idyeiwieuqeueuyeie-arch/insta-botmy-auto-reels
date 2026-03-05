import os
import time
import random
import threading
from instagrapi import Client
from datetime import datetime, timedelta
from flask import Flask

# --- 1. كود الحفاظ على عمل السيرفر (ضروري لـ Render) ---
app = Flask('')

@app.route('/')
def home(): 
    return "Bot is Running Live!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- 2. بياناتك الأساسية ---
USER = "ug.31"
PASS = ".736alameri."
SEARCH_KEYWORDS = ["نصائح", "حكم", "عبارات"] 
FIXED_COMMENT = "تابعني للمزيد لطفا ❤️"

cl = Client()

def run_bot():
    print("...جاري بدء محرك البوت")
    try:
        # محاولة تسجيل الدخول
        cl.login(USER, PASS)
        print("تم تسجيل الدخول بنجاح ✅")
    except Exception as e:
        print(f"خطأ في الدخول: {e}")
        return

    posted_today = 0
    active_posts = []

    while True:
        try:
            # 1. البحث والنشر (3 ريلزات في اليوم)
            if posted_today < 3:
                tag = random.choice(SEARCH_KEYWORDS)
                print(f"جاري البحث في هاشتاج #{tag}...")
                
                medias = cl.hashtag_medias_top(tag, amount=7)
                for m in medias:
                    if m.view_count > 500000 and m.media_type == 2:
                        print(f"تم العثور على ريلز لقطة! مشاهداته: {m.view_count}")
                        
                        # تحميل الفيديو
                        path = cl.video_download(m.pk, "./temp")
                        final_caption = f"{m.caption_text}\n.\n{FIXED_COMMENT}"
                        
                        print("جاري الرفع الآن...")
                        new_reels = cl.video_upload(path, final_caption)
                        
                        active_posts.append({
                            'id': new_reels.pk, 
                            'time': datetime.now()
                        })
                        
                        posted_today += 1
                        if os.path.exists(path):
                            os.remove(path)
                        
                        print(f"تم النشر! العدد الحالي لليوم: {posted_today}")
                        time.sleep(14400) # انتظار 4 ساعات قبل الفيديو القادم
                        break
            
            # 2. فحص الحذف أو المراقبة (اختياري)
            for p in active_posts[:]:
                if datetime.now() - p['time'] > timedelta(hours=1):
                    active_posts.remove(p)

            # تصفير العداد عند بداية يوم جديد
            if datetime.now().hour == 0:
                posted_today = 0
                
            time.sleep(60)
        except Exception as e:
            print(f"حدث خطأ أثناء العمل: {e}")
            time.sleep(60)

# --- 3. التشغيل المتوازي (المفتاح السحري) ---
if __name__ == "__main__":
    # تشغيل البوت في "خيط" منفصل ليعمل في الخلفية
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # تشغيل سيرفر الويب (هذا ما يبحث عنه موقع Render ليقول Live)
    run_web_server()
    
  
