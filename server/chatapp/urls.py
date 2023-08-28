from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('chat/', views.interact_with_ai, name='chat'),
    path('user/',views.get_calls_made,name='user'),
]