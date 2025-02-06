from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # لإحضار AUTH_USER_MODEL
import uuid
from django.utils import timezone
from django.db import transaction



class CustomUserManager(models.Manager):
    @transaction.atomic
    def get_users_by_group(self, group_name):
        """إرجاع المستخدمين الذين ينتمون إلى مجموعة معينة"""
        return self.filter(groups__name=group_name)
    
    @transaction.atomic
    def get_users_with_permission(self, permission_name):
        """إرجاع المستخدمين الذين لديهم إذن معين"""
        return self.filter(user_permissions__codename=permission_name)
    
    @transaction.atomic
    def get_by_natural_key(self, username):
        """إرجاع المستخدم باستخدام اسم المستخدم"""
        return self.get(username=username)
    
        
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    # تعيين المدير المخصص للموديل
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class TeamMemberManager(models.Manager):
    @transaction.atomic
    def get_by_role(self, role_name):
        """إرجاع أعضاء الفريق بناءً على دورهم"""
        return self.filter(role=role_name)
    
    @transaction.atomic
    def get_all_members(self):
        """إرجاع جميع أعضاء الفريق"""
        return self.all()



class TeamMember(models.Model):
    name = models.CharField(max_length=100)  # اسم العضو
    role = models.CharField(max_length=100)  # دور العضو
    image = models.ImageField(upload_to='team_images/')  # صورة العضو

    # تعيين المدير المخصص للموديل
    objects = TeamMemberManager()

    def __str__(self):
        return self.name
        

class PostManager(models.Manager):
    @transaction.atomic
    def top_rated(self):
        """إرجاع المنشورات التي تمتلك أعلى التقييمات"""
        return self.filter(rating__gt=0).order_by('-rating')
    
    @transaction.atomic
    def recent_posts(self):
        """إرجاع المنشورات التي تم إنشاؤها مؤخرًا"""
        return self.order_by('-created')

    @transaction.atomic
    def posts_by_author(self, author):
        """إرجاع المنشورات التي كتبها مؤلف معين"""
        return self.filter(author=author)

        

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.URLField(max_length=500, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="posts")
    rating = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    # تعيين المدير المخصص للموديل
    objects = PostManager()

    def __str__(self):
        return self.title



class TagManager(models.Manager):
    @transaction.atomic
    def ordered(self):
        """إرجاع العلامات مرتبة حسب الحقل 'order'"""
        return self.order_by('order')
    

    @transaction.atomic
    def with_image(self):
        """إرجاع العلامات التي تحتوي على صورة"""
        return self.filter(image__isnull=False)
    

    @transaction.atomic
    def by_name(self, name):
        """إرجاع العلامات التي تحتوي على اسم معين"""
        return self.filter(name__icontains=name)



class Tag(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)

    # تعيين المدير المخصص للموديل
    objects = TagManager()

    def __str__(self):
        return self.name



class CommentManager(models.Manager):
    @transaction.atomic
    def recent_comments(self):
        """إرجاع التعليقات التي تم إنشاؤها مؤخرًا"""
        return self.order_by('-created')
    
    @transaction.atomic
    def comments_by_author(self, author):
        """إرجاع التعليقات التي كتبها مؤلف معين"""
        return self.filter(author=author)
    
    @transaction.atomic
    def comments_for_post(self, post):
        """إرجاع التعليقات المرتبطة بمنشور معين"""
        return self.filter(parent_post=post)





class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # الإشارة إلى نموذج المستخدم المخصص
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments'
    )
    parent_post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # تعيين المدير المخصص للموديل
    objects = CommentManager()

    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}'
        except AttributeError:
            return f'Unknown Author: {self.body[:30]}'





class NewsItemManager(models.Manager):
    @transaction.atomic
    def recent_news(self):
        """إرجاع الأخبار الأحدث حسب تاريخ الإنشاء"""
        return self.order_by('-created_at')
    
    @transaction.atomic
    def top_rated(self):
        """إرجاع الأخبار الأعلى تقييمًا (من الأعلى إلى الأدنى)"""
        return self.filter(rating__gte=4).order_by('-rating')

    @transaction.atomic
    def news_by_publish_date(self):
        """إرجاع الأخبار حسب تاريخ النشر"""
        return self.filter(publish_date__isnull=False).order_by('-publish_date')





class NewsItem(models.Model):
    name = models.CharField(max_length=200)  # اسم الشخص في الخبر
    job_title = models.CharField(max_length=200)  # الوظيفة
    description = models.TextField()  # وصف الخبر
    image = models.ImageField(upload_to='news_images/')  # صورة الشخص
    rating = models.PositiveIntegerField(default=5)  # التقييم بالنجوم (من 1 إلى 5)
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ إضافة الخبر
    publish_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # جعل الحقل يقبل القيم الفارغة
    link = models.URLField(max_length=200, null=True, blank=True)

    # تعيين المدير المخصص للموديل
    objects = NewsItemManager()

    def __str__(self):
        return self.name




class NewsManager(models.Manager):
    @transaction.atomic
    def top_rated(self):
        """إرجاع الأخبار ذات التقييم الأعلى"""
        return self.filter(rating__gte=4).order_by('-rating')
    

    @transaction.atomic
    def news_with_image(self):
        """إرجاع الأخبار التي تحتوي على صورة"""
        return self.filter(image__isnull=False)


    @transaction.atomic
    def recent_news(self):
        """إرجاع الأخبار حسب التقييم الأحدث"""
        return self.order_by('-rating')  # ترتيب الأخبار حسب التقييم (من الأعلى إلى الأدنى)





class News(models.Model):
    name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=100)
    rating = models.IntegerField()  # التقييم، الذي يكون عدد النجوم
    description = models.TextField()  # الوصف
    image = models.ImageField(upload_to='news_images/')  # صورة الخبر

    # تعيين المدير المخصص للموديل
    objects = NewsManager()

    def __str__(self):
        return self.name



class MemberManager(models.Manager):
    @transaction.atomic
    def by_email(self, email):
        """إرجاع عضو حسب البريد الإلكتروني"""
        return self.filter(email=email)


    @transaction.atomic
    def active_members(self):
        """إرجاع الأعضاء الذين لديهم كلمة مرور معينة (مثال: كلمة مرور غير فارغة)"""
        return self.filter(password__isnull=False)


    @transaction.atomic
    def ordered_members(self):
        """إرجاع الأعضاء مرتبين حسب الاسم"""
        return self.order_by('name')

class Member(models.Model):
    name = models.CharField(max_length=100, default="Unnamed")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    # تعيين المدير المخصص للموديل
    objects = MemberManager()

    def __str__(self):
        return self.name


   


class ProgressManager(models.Manager):
    @transaction.atomic
    def add_or_update_progress(self, **kwargs):
        """
        إضافة أو تحديث التقدّم.
        إذا كان هناك سجل يتطابق مع الشرط، يتم تحديثه.
        إذا لم يكن موجودًا، يتم إنشاؤه.
        
        kwargs: القيم التي سيتم التحقق منها وإضافتها أو تحديثها.
        """
        # تحديد القيم المستخدمة للبحث
        lookup_fields = kwargs.get('lookup', {})
        
        # إزالة `lookup` من kwargs لأنه لا يستخدم في التحديث أو الإنشاء
        data = {key: value for key, value in kwargs.items() if key != 'lookup'}
        
        # إنشاء أو تحديث السجل
        instance, created = self.update_or_create(defaults=data, **lookup_fields)
        return instance  # نرجع الكائن فقط وليس tuple

from django.db import models

from django.db import models

class Progress(models.Model):
    partner = models.IntegerField(default=0)
    employee = models.IntegerField(default=0)
    client = models.IntegerField(default=0)
    job = models.IntegerField(default=0)

    def __str__(self):
        return f"Progress: Partner {self.partner}%, Employee {self.employee}%, Client {self.client}%, Job {self.job}%"




class MessageManager(models.Manager):
    @transaction.atomic
    def sent_by_user(self, user):
        """إرجاع الرسائل التي أرسلها مستخدم معين"""
        return self.filter(sender=user)


    @transaction.atomic
    def messages_in_last_days(self, days):
        """إرجاع الرسائل التي تم إرسالها في الأيام الأخيرة"""
        time_limit = timezone.now() - timezone.timedelta(days=days)
        return self.filter(date__gte=time_limit)
     

    @transaction.atomic
    def recent_messages(self):
        """إرجاع الرسائل التي تم إرسالها في الفترة الأخيرة (مثال: آخر 7 أيام)"""
        return self.messages_in_last_days(7)


    @transaction.atomic
    def ordered_by_date(self):
        """إرجاع الرسائل مرتبة حسب التاريخ من الأحدث للأقدم"""
        return self.order_by('-date')

class Message(models.Model):
    text = models.TextField()  # نص الرسالة
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)  # تاريخ الإرسال

    # تعيين المدير المخصص للموديل
    objects = MessageManager()

    def __str__(self):
        return f"Message from {self.sender.username} on {self.date}"





        


class ContactMessage(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)  # تأكد من وجود هذا الحقل

    # تعريف المدير المخصص داخل الكلاس
    class MessageManager(models.Manager):
        @transaction.atomic
        def recent(self):
            """إرجاع الرسائل التي تم إرسالها في آخر 7 أيام"""
            seven_days_ago = timezone.now() - timezone.timedelta(days=7)
            return self.filter(date_sent__gte=seven_days_ago)

    # تعيين المدير المخصص للموديل
    objects = models.Manager()  # المدير الافتراضي
    recent_messages = MessageManager()  # المدير المخصص للرسائل الأحدث

    # تعريف دالة __str__ واحدة فقط
    def __str__(self):
        return f"Message from {self.name} at {self.date_sent}"
