from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # الصفحة الرئيسية
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('page/', views.page, name='page'),
    path('Contactus/', views.contactus, name='Contactus'),
    path('depar/', views.depar, name='depar'),
    path('home/', views.home, name='home'),
    path('services1/', views.services1, name='services1'),
    path('services2/', views.services2, name='services2'),
    path('services3/', views.services3, name='services3'),
    path('services4/', views.services4, name='services4'),
    path('services5/', views.services5, name='services5'),
    path('services6/', views.services6, name='services6'),
    path('services7/', views.services7, name='services7'),
    path('services8/', views.services8, name='services8'),
    path('services9/', views.services9, name='services9'),
]
