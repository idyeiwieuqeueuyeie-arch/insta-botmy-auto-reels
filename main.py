import os
import time
import random
from instagrapi import Client
from datetime import datetime, timedelta
from flask import Flask
import threading

# --- 1. كود الحفاظ على عمل السيرفر (ضروري لـ Render) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Running"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run).start()

# --- 2. بياناتك الأساسية ---
USER = "ug.31"
PASS = ".736alameri."
SEARCH_KEYWORDS = ["نصائح", "حكم", "عبارات"] 
FIXED_COMMENT = "تابعني للمزيد لطفا ❤️"

cl = Client()

def run_bot():
    print("جاري بدء البوت...")
    try:
        cl.login(USER, PASS)
        print("تم تسجيل الدخول بنجاح ✅")
    except Exception as e:
        print(f"خطأ في الدخول: {e}")
        return

    posted_today = 0
    active_posts = []

    while True:
        # 1. البحث والنشر (3 ريلزات في اليوم)
        if posted_today < 3:
            tag = random.choice(SEARCH_KEYWORDS)
            print(f"جاري البحث في هاشتاج #{tag}...")
            
            try:
                medias = cl.hashtag_medias_top(tag, amount=7)
                for m in medias:
                    if m.view_count > 500000 and m.media_type == 2:
                        print(f"تم العثور على ريلز لقطة! مشاهداته: {m.view_count}")
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
                        time.sleep(14400) # انتظار 4 ساعات
                        break
            except Exception as e:
                print(f"حدث خطأ أثناء البحث أو الرفع: {e}")

        # 2. فحص الحذف بعد ساعة (تنظيف المنشورات القديمة إذا أردت)
        for p in active_posts[:]:
            if datetime.now() - p['time'] > timedelta(hours=1):
                try:
                    # تم إغلاق الشرط هنا لتجنب الخطأ السابق
                    print(f"مرت ساعة على المنشور {p['id']}")
                    active_posts.remove(p)
                except Exception as e:
                    print(f"خطأ في المعالجة: {e}")

        # تصفير العداد اليومي عند بداية يوم جديد
        if datetime.now().hour == 0:
            posted_today = 0
            
        time.sleep(60)

if __name__ == "__main__":
    run_bot()
  
