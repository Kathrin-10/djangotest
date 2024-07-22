from django.urls import path
from . import views
from .views import forgot_password

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index, name='index'),
    path('chat/<int:friend_id>/', views.chat, name='chat'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    
]

