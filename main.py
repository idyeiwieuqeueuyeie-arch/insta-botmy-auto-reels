import os
import time
import random
from instagrapi import Client
from datetime import datetime, timedelta
import os
import time
import random
from instagrapi import Client
from datetime import datetime, timedelta

# --- بياناتك الأساسية (عدلها بعناية) ---
USER = "ug.31"
PASS = ".736alameri."
# الكلمات التي سيبحث البوت عن فيديوهات من خلالها
SEARCH_KEYWORDS = ["نصائح","حكم", "عبارات"] 
FIXED_COMMENT = "تابعني للمزيد لطفا ❤️"

cl = Client()

def run_bot():
    print("جاري بدء البوت...")
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
        now = datetime.now()

        # 1. البحث والنشر (3 ريلزات في اليوم)
        if posted_today < 3:
            tag = random.choice(SEARCH_KEYWORDS)
            print(f"جاري البحث في هاشتاج #{tag}...")
            
            try:
                # جلب أفضل المنشورات في هذا الهاشتاج
                medias = cl.hashtag_medias_top(tag, amount=7)
                
                for m in medias:
                    # التحقق: مشاهدات فوق 500 ألف ونوع الملف فيديو (ريلز)
                    if m.view_count > 500000 and m.media_type == 2:
                        print(f"تم العثور على ريلز لقطة! مشاهداته: {m.view_count}")
                        
                        # تحميل الفيديو
                        path = cl.video_download(m.pk, "./temp")
                        
                        # سحب الهاشتاجات الأصلية + إضافة تعليقك
                        # m.caption_text يجلب النص الأصلي مع هاشتاجاته
                        final_caption = f"{m.caption_text}\n.\n{FIXED_COMMENT}"
                        
                        # عملية الرفع
                        print("جاري الرفع الآن...")
                        new_reels = cl.video_upload(path, final_caption)
                        
                        # إضافة المنشور لقائمة المراقبة للحذف بعد ساعة
                        active_posts.append({
                            'id': new_reels.pk, 
                            'time': datetime.now()
                        })
                        
                        posted_today += 1
                        os.remove(path) # حذف الملف المؤقت من السيرفر
                        print(f"تم النشر! العدد الحالي لليوم: {posted_today}")
                        
                        # انتظار 4 ساعات قبل البحث عن الفيديو التالي لكي لا يحظر الحساب
                        time.sleep(14400) 
                        break
            except Exception as e:
                print(f"حدث خطأ أثناء البحث أو الرفع: {e}")

        # 2. فحص التفاعل والحذف بعد ساعة
        for p in active_posts[:]:
            if datetime.now() - p['time'] > timedelta(hours=1):
                try:
                    info = cl.media_info(p['id'])
                    # شرط
