from user_management.models import TeamMember, Post, NewsItem
from user_management.models import Progress  # تأكد من أن المسار صحيح حسب مكان وجود النموذج


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book


# عرض الصفحة الرئيسية
def index(request):
    # جلب جميع البيانات المطلوبة
    team_members = TeamMember.objects.all()  # جلب كل أعضاء الفريق
    posts = Post.objects.all()  # جلب كل المنشورات
    news_items = NewsItem.objects.all()  # جلب جميع الأخبار

    # استرجاع القيم من قاعدة البيانات
    progress = Progress.objects.first()
    if not progress:
        progress = Progress.objects.create(partner=0, employee=0, client=0, job=0)

    # تقسيم الأعضاء إلى مجموعات تحتوي على 3 أعضاء في كل مجموعة
    team_groups = [team_members[i:i + 3] for i in range(0, len(team_members), 3)]

    return render(request, 'pages/index.html', {
        'team_groups': team_groups,  # تمرير الأعضاء بشكل مجموعات
        'posts': posts,
        'news_items': news_items,
        'progress': progress,  # القيم المعروضة في الصفحة
    })

# عرض صفحة "عن الموقع"
def about(request):
    return render(request, 'pages/about.html')


# عرض صفحة التاريخ
def history(request):
    return render(request, 'pages/history.html')


# عرض صفحة "depart"
def depar(request):
    return render(request, 'pages/depar.html')


# عرض صفحة معينة
def page(request):
    return render(request, 'pages/page.html')


# عرض صفحة الاتصال بنا
def contactus(request):
    return render(request, 'pages/contactus.html')


def services1(request):
    return render(request, 'pages/services1.html')
def services2(request):
    return render(request, 'pages/services2.html')
def services3(request):
    return render(request, 'pages/services3.html')
def services4(request):
    return render(request, 'pages/services4.html')
def services5(request):
    return render(request, 'pages/services5.html')
def services6(request):
    return render(request, 'pages/services6.html')
def services7(request):
    return render(request, 'pages/services7.html')
def services8(request):
    return render(request, 'pages/services8.html')
def services9(request):
    return render(request, 'pages/services9.html')
def home(request):
    return render(request, 'pages/home.html')


# إضافة عضو جديد
