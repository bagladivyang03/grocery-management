from django.contrib import admin
from django.urls import path, include, re_path
from grocery_management import views
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .views import ItemView, cartItemsView

app_name = 'grocery_management'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('about/', login_required(views.AboutView.as_view()), name='aboutus'),
    path('home/', views.homepage, name='homepage'),
    # path('contactus/',views.ContactUsView.as_view(),name='contactus'),
    path('contactus/', views.contact_us, name='contactus'),
    path('viewprofile/', views.view_profile, name='viewprofile'),
    path('cart/', login_required(views.CartView.as_view()), name='cartview'),
    path('products/', login_required(views.ProductView.as_view()), name='productview'),
    path('getAllItems/', ItemView.as_view(), name='getAllItems'),
    path('getAllItems/addToCart/<int:id>',
         views.addToCart, name='addItemToCart'),
     path('home/addToCart/<int:id>',views.addToCart,name='addItemToCart'),
    path('getMyCart', login_required(cartItemsView.as_view()), name='getMyCart'),
    path('deleteItem/<int:id>',
         views.removeItemFromCart, name='remvoeItemFromCart'),
    path('search/<str:string>', views.search, name='search'),
    path('getAllProducts/', views.getitems, name='getProducts')
]
