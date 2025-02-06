from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # مسار لوحة التحكم الخاصة بـ admin
    path('admin/', admin.site.urls),
    
    # توجيه المسارات إلى التطبيق pages
    path('', include('pages.urls')),  # صفحة البداية
    path('ad/', include('user_management.urls')),  # التأكد من أن 'ad/' متطابق مع المسار
]

# إضافة إعدادات الميديا لتخزين الملفات
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
