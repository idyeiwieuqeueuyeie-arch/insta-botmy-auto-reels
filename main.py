import os
import time
import random
import threading
from instagrapi import Client
from flask import Flask

# 1. إنشاء واجهة السيرفر لضمان بقائه نشطاً
app = Flask('')
@app.route('/')
def home(): 
    return "<h1>البوت نشط! جاري البحث عن ريلز ملاحظات آيفون...</h1>"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. بيانات الحساب والكلمات الدلالية
USER = "ug.31"
PASS = ".736alameri."
# كلمات البحث للوصول لريلز ملاحظات آيفون وموسيقى هادئة
KEYWORDS = ["ملاحظات_ايفون", "iphone_notes", "خواطر_عتاب", "عبارات_حزينه", "ستوريات_انستا"]
# الهاشتاجات المشهورة للنشر
TREND_TAGS = "#اكسبلور #explore #ترند #ملاحظات_ايفون #ستوريات #اقتباسات #foryou #انستقرام"

cl = Client()

def start_bot():
    print("🚀 جاري محاولة الدخول وإصلاح خطأ الإعدادات...")
    try:
        # إصلاح الخطأ: تعريف الجهاز بطريقة متوافقة مع السيرفر
        cl.set_device_settings({
            "manufacturer": "Apple",
            "model": "iPhone 13 Pro",
            "android_version": 26,
            "android_release": "8.0.0"
        })
        cl.login(USER, PASS)
        print("✅✅ تم تسجيل الدخول بنجاح!")
    except Exception as e:
        print(f"⚠️ فشل الدخول بالإعدادات، محاولة دخول مباشر: {e}")
        try:
            cl.login(USER, PASS)
            print("✅ تم الدخول المباشر!")
        except Exception as e2:
            print(f"❌ فشل نهائي في الدخول: {e2}")
            return

    while True:
        try:
            tag = random.choice(KEYWORDS)
            print(f"🔍 البحث عن صيد ثمين في هاشتاج: #{tag}...")
            # البحث في الهاشتاج عن أحدث الريلز
            medias = cl.hashtag_medias_recent(tag, amount=15)
            
            for m in medias:
                # التحقق من أن المقطع فيديو (ريلز) وبمشاهدات جيدة (أكثر من 20 ألف للسرعة)
                if m.media_type == 2 and m.view_count > 20000:
                    print(f"🎯 وجدنا ريلز لقطة! مشاهدات: {m.view_count}")
                    
                    # تحميل المقطع
                    path = cl.video_download(m.pk, "./temp")
                    
                    # صياغة النص (الكابشن)
                    caption = f"اقتباس اليوم ✨\n.\n{TREND_TAGS}"
                    
                    # رفع المقطع
                    cl.video_upload(path, caption)
                    print("🎉 تم النشر بنجاح على حسابك!")
                    
                    # تنظيف الملفات المؤقتة
                    if os.path.exists(path):
                        os.remove(path)
                    
                    # انتظار 3 ساعات قبل النشر التالي لضمان الأمان
                    print("😴 انتظار 3 ساعات للمحافظة على أمان الحساب...")
                    time.sleep(10800)
                    break
            
            # إذا لم يجد فيديو مناسب، ينتظر 10 دقائق ويعيد البحث في هاشتاج آخر
            time.sleep(600)
            
        except Exception as e:
            print(f"⚠️ تنبيه بسيط: {e}")
            time.sleep(900)

if __name__ == "__main__":
    # تشغيل السيرفر في خيط (Thread) منفصل
    threading.Thread(target=run_web, daemon=True).start()
    # تشغيل البوت
    start_bot()
    
