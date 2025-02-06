from django import forms
from .models import TeamMember


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'image']
from django import forms
from .models import Post

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'rating']  # تأكد من أن الحقول التي تحددها هنا موجودة في نموذج Post

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']  # حقل الجسم فقط للتعليق


# forms.py

from django import forms
from .models import NewsItem

class NewsItemForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ['name', 'job_title', 'description', 'image', 'rating', 'link',]

from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

# user_management/forms.py

from django import forms

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
