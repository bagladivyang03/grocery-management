from django.contrib import admin
from django.urls import path,include
from grocery_management import views
from django.urls import reverse_lazy


app_name = 'grocery_management'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    
]