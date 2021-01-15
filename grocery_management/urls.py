from django.contrib import admin
from django.urls import path,include,re_path
from grocery_management import views
from django.urls import reverse_lazy


app_name = 'grocery_management'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('about/',views.AboutView.as_view(),name='aboutus'),
    path('home/',views.HomePageView.as_view(),name='homepage'),
    # path('contactus/',views.ContactUsView.as_view(),name='contactus'),
    path('contactus/',views.contact_us,name='contactus'),
    path('viewprofile/',views.view_profile,name='viewprofile'),
]