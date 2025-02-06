from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-member/', views.add_member, name='add_member'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('Contactus/', views.contactus, name='Contactus'),
    path('messages/', views.message_list, name='message_list'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add-team-member/', views.add_team_member, name='add_team_member'),
    path('delete-team-member/<int:member_id>/', views.delete_team_member, name='delete_team_member'),
    path('create/', views.create_post, name='create_post'),
    path('update_progress/', views.update_progress, name='update_progress'),
    path('add_news_item/', views.add_news_item, name='add_news_item'),
    path('delete_news_item/<int:news_id>/', views.delete_news_item, name='delete_news_item'),
]
