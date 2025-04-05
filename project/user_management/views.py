from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    ContactMessage, TeamMember, Post, NewsItem, CustomUser, Member
)
from .forms import (
    TeamMemberForm, PostForm, NewsItemForm, ContactForm, ContactUsForm
)

# عرض الصفحة الرئيسية
def index(request):
    team_members = TeamMember.objects.all()
    posts = Post.objects.all()
    news_items = NewsItem.objects.all()

    progress = {
        'partner': request.session.get('partner', 0),
        'employee': request.session.get('employee', 0),
        'client': request.session.get('client', 0),
        'job': request.session.get('job', 0),
    }

    for news in news_items:
        news.stars = range(news.rating)

    team_groups = [team_members[i:i + 3] for i in range(0, len(team_members), 3)]

    return render(request, 'pages/index.html', {
        'team_groups': team_groups,
        'posts': posts,
        'news_items': news_items,
        'progress': progress,
    })

# تحديث القيم المخزنة
def update_progress(request):
    if request.method == 'POST':
        request.session['partner'] = request.POST.get('partner', 0)
        request.session['employee'] = request.POST.get('employee', 0)
        request.session['client'] = request.POST.get('client', 0)
        request.session['job'] = request.POST.get('job', 0)
        return redirect('index')

    progress = {
        'partner': request.session.get('partner', 0),
        'employee': request.session.get('employee', 0),
        'client': request.session.get('client', 0),
        'job': request.session.get('job', 0),
    }

    return render(request, 'pages/update_progress.html', {'progress': progress})

# إضافة عضو جديد
def add_member(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not Member.objects.filter(email=email).exists():
            Member.objects.create(name=name, email=email, password=password)
            return JsonResponse({"message": "Member added successfully!"})
        return JsonResponse({"message": "Email already exists!"}, status=400)

    return render(request, 'pages/member_form.html')

# تسجيل الدخول
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'pages/login.html', {'error': 'يرجى ملء جميع الحقول'})

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'pages/login.html', {'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'})

    return render(request, 'pages/login.html')

# تسجيل الخروج
def logout_view(request):
    logout(request)
    return redirect('pages/login')

# لوحة التحكم
@login_required
def dashboard(request):
    members = TeamMember.objects.all()
    news_items = NewsItem.objects.all()
    contact_messages = ContactMessage.objects.all().order_by('-date_sent')
    

    progress = {
        'partner': request.session.get('partner', 0),
        'employee': request.session.get('employee', 0),
        'client': request.session.get('client', 0),
        'job': request.session.get('job', 0),
    }

    return render(request, 'pages/dashboard.html', {
        'members': members,
        'news_items': news_items,
        'progress': progress,
        'contact_messages': contact_messages,
    })

# حذف مستخدم
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('pages/dashboard')

# إضافة مستخدم مخصص
def add_custom_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not CustomUser.objects.filter(email=email).exists():
            CustomUser.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"message": "User added successfully!"})
        return JsonResponse({"message": "Email already exists!"}, status=400)

    return render(request, 'pages/custom_user_form.html')

# حذف عضو
@login_required
def delete_team_member(request, member_id):
    member = get_object_or_404(TeamMember, id=member_id)
    member.delete()
    return redirect('dashboard')

# إضافة عضو جديد باستخدام النموذج
@login_required
def add_team_member(request):
    if request.method == "POST":
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إضافة العضو بنجاح!")
            return redirect('index')
    else:
        form = TeamMemberForm()

    return render(request, 'pages/add_team_member.html', {'form': form})

# إنشاء منشور جديد
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()

    return render(request, 'pages/create_post.html', {'form': form})

# إضافة خبر جديد
@login_required
def add_news_item(request):
    if request.method == "POST":
        form = NewsItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إضافة الخبر بنجاح!")
            return redirect('index')
    else:
        form = NewsItemForm()

    return render(request, 'pages/add_news_item.html', {'form': form})

# حذف خبر
@login_required
def delete_news_item(request, news_id):
    news_item = get_object_or_404(NewsItem, id=news_id)
    news_item.delete()
    messages.success(request, "تم حذف الخبر بنجاح!")
    return redirect('dashboard')

# إرسال رسالة اتصال
def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # إضافة رسالة نجاح
            messages.success(request, 'تم إرسال رسالتك بنجاح!')
        else:
            # إضافة رسالة خطأ
            messages.error(request, 'حدث خطأ أثناء إرسال الرسالة. يرجى التحقق من الحقول وإعادة المحاولة.')

    return render(request, 'pages/Contactus.html', {'form': ContactForm()})

# عرض الرسائل
def message_list(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'pages/messages.html', {'messages': messages})

# نموذج الاتصال
def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ContactUsForm()

    return render(request, 'pages/contactus.html', {'form': form})
from django.shortcuts import redirect

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.delete()
    messages.success(request, 'تم حذف الرسالة بنجاح!')
    return redirect('dashboard')  # استبدل 'dashboard' برابط لوحة التحكم إذا كان مختلفًا
