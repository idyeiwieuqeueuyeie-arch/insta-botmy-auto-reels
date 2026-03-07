import os
import time
import random
import threading
from instagrapi import Client
from flask import Flask

# 1. إعداد السيرفر
app = Flask('')
@app.route('/')
def home(): 
    return "<h1>البوت يعمل بنظام الأمان: 3 ريلزات يومياً 🛡️</h1>"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. معلومات الحساب
USER = "ug.31"
PASS = ".736alameri."
KEYWORDS = ["ملاحظات_ايفون", "iphone_notes", "اقتباسات_حزينة", "ستوريات_انستا"]
TREND_TAGS = "#اكسبلور #explore #ملاحظات_ايفون #اقتباسات #foryou"

cl = Client()

def start_bot():
    print("🚀 بدء التشغيل بنظام 3 منشورات يومياً...")
    try:
        cl.login(USER, PASS)
        print("✅✅ تم تسجيل الدخول بنجاح!")
    except Exception as e:
        print(f"❌ خطأ في الدخول: {e}")
        return

    while True:
        try:
            tag = random.choice(KEYWORDS)
            print(f"🔍 فحص الهاشتاج: #{tag}")
            medias = cl.hashtag_medias_recent(tag, amount=10)
            
            for m in medias:
                # شرط مشاهدات معقول لضمان جودة المحتوى
                if m.media_type == 2 and m.view_count > 5000:
                    print(f"🎯 وجدنا فيديو مناسب ({m.view_count} مشاهدة)")
                    path = cl.video_download(m.pk, "./temp")
                    caption = f"اقتباس اليوم ✨\n.\n{TREND_TAGS}"
                    cl.video_upload(path, caption)
                    print("🎉 تم النشر بنجاح!")
                    if os.path.exists(path): os.remove(path)
                    
                    # الانتظار لمدة 8 ساعات (لضمان 3 منشورات فقط في 24 ساعة)
                    print("😴 نظام الأمان: انتظار 8 ساعات للمنشور القادم...")
                    time.sleep(28800) 
                    break
            
            time.sleep(600) # فحص كل 10 دقائق إذا لم يجد فيديو
        except Exception as e:
            print(f"⚠️ تنبيه: {e}")
            time.sleep(900)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    start_bot()
