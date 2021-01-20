from django.shortcuts import render, redirect
from grocery_management.forms import UserForm, CustomerInfoForm, ContactUsForm, UpdateInfoForm
from grocery_management.models import CustomerRegistration
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .serializer import CustomerRegistrationSerializer
from django.contrib import messages
from . import mailhandler
from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.core import serializers
from datetime import datetime
from django.contrib import messages
# Create your views here.


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        customer_info_form = CustomerInfoForm(data=request.POST)
        if user_form.is_valid() and customer_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            customer_info = customer_info_form.save(commit=False)
            customer_info.user = user
            customer_info.save()
            registered = True
            return redirect('grocery_management:login')
    else:
        user_form = UserForm()
        customer_info_form = CustomerInfoForm()

    return render(request, 'grocery_management/index.html', {'user_form': user_form, 'customer_info_form': customer_info_form, 'registered': registered})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("grocery_management:homepage")
    else:
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    request.session['user_id'] = request.user.id
                    login(request, user)
                    return redirect("grocery_management:homepage")
                else:
                    messages.info(request, "Account doesn't exists")
            else:
                messages.info(request, 'Username or Password Incorrect')
                # print("Someone tried to login and failed!")
                # print("Username: {} and password {}".format(username, password))
                # return HttpResponse("invalid login details supplied!")
        return render(request, 'grocery_management/login.html',{})


@login_required
def user_logout(request):
    request.session.flush()
    logout(request)
    return HttpResponseRedirect(reverse('grocery_management:login'))


class AboutView(TemplateView):
    template_name = 'grocery_management/about.html'


class HomePageView(TemplateView):
    template_name = 'grocery_management/homepage.html'

# class ContactUsView(TemplateView):
#     template_name = 'grocery_management/contactus.html'


@login_required
def contact_us(request):

    message_sent = False
    if request.method == "POST":
        contact_us_form = ContactUsForm(data=request.POST)

        if contact_us_form.is_valid():

            sender_name = contact_us_form.cleaned_data['fullname']
            sender_email = contact_us_form.cleaned_data['email']
            sender_subject = contact_us_form.cleaned_data['subject']
            sender_message = contact_us_form.cleaned_data['message']
            mailhandler.sendMailToUser(sender_name, sender_email)
            mailhandler.sendMailToGMS(
                sender_name, sender_email, sender_subject, sender_message)
            # message = "{0} has sent you a new message:\n\n{1}".format(sender_name,contact_us_form.cleaned_data['subject'], contact_us_form.cleaned_data['message'])
            # send_mail('New Enquiry', message, sender_email, ['bagladivyang03@gmail.com'])
            contact_us_form.save()
            message_sent = True
    else:
        contact_us_form = ContactUsForm()

    return render(request, 'grocery_management/contactus.html', {'contact_us_form': contact_us_form, 'message_sent': message_sent})


# class view_profile(TemplateView):
#     template_name = 'grocery_management/viewprofile.html'
@login_required
def view_profile(request):
    customer_info = CustomerRegistration.objects.get(user_id=request.user.id)
    print(customer_info)
    print(customer_info.street)
    update_form = UpdateInfoForm(instance=customer_info)
    print(update_form)
    # print(update_form.mobile)
    if request.method=="POST":
        update_form = UpdateInfoForm(request.POST,instance=customer_info)
        if update_form.is_valid():
            update_form.save()
            messages.success(request,"Your profile is updated successfully!!",extra_tags='alert-success')
    return render(request, 'grocery_management/viewprofile.html', {'customer_info': customer_info,'update_form':update_form})


class CartView(TemplateView):
    template_name = 'grocery_management/cart.html'


class ProductView(TemplateView):
    template_name = 'grocery_management/products.html'


class ItemView(APIView):
    def get(self, request):
        getAllItems = Item.objects.all()
        itemset = ItemSerializer(getAllItems, many=True)
        return render(request, 'grocery_management/products.html', {'Items': getAllItems})
        # return Response(itemset.data)


@login_required
def addToCart(request, id):
    print(request.user.id)
    UserCartExists = Cart.objects.filter(user=request.user.id).exists()
    if not UserCartExists:
        cart_obj = Cart()
        cart_obj.user = request.user
        cart_obj.ordered = False
        cart_obj.total_price = 0
        cart_obj.save()
    userCartReference = Cart.objects.get(user=request.user.id)
    getitem = Item.objects.get(id=id)
    itemRef = CartItems()
    itemRef.cart = userCartReference
    itemRef.user = request.user
    itemRef.item = getitem
    itemRef.price = getitem.price
    itemRef.quantity = 1
    itemRef.save()
    messages.info(request, 'Item Added to Cart')
    return redirect('grocery_management:getAllItems')


class cartItemsView(APIView):
    def get(self, request):
        print(request.user.id)
        userCart = CartItems.objects.filter(
            user_id=request.user.id).prefetch_related().values('id', 'price', 'quantity', 'cart_id', 'cart_id__total_price', 'user_id', 'item__item_name', 'item__image', 'item_id__price', 'item_id__colour_type_id__colour_name', 'item_id__quantity_type_id__variant_name', 'item_id__size_type_id__size_name', 'item_id__description', 'item_id__quantity_available')
        jsonRes = []
        for res in userCart:
            if res['item_id__colour_type_id__colour_name'] == None:
                res['item_id__colour_type_id__colour_name'] = 'Not Applicable'
            if res['item_id__quantity_type_id__variant_name'] == None:
                res['item_id__quantity_type_id__variant_name'] = 'Not Applicable'
            if res['item_id__size_type_id__size_name'] == None:
                res['item_id__size_type_id__size_name'] = 'Not Applicable'
            jsonRes.append(res)
        cartItemsDetails = jsonRes
        lengthofCartItemDetails = len(jsonRes)
        total_amount = jsonRes[lengthofCartItemDetails -
                               1]['cart_id__total_price']
        total_amount_with_gst = total_amount+((total_amount*5)/100)
        expected_delivery = str(datetime.today()).split()[0]
        customer_info = CustomerRegistration.objects.get(
            user_id=request.user.id)
        print(cartItemsDetails)
        context = {'cartItemsDetails': cartItemsDetails,
                   'lengthofCartItemDetails': lengthofCartItemDetails,
                   'total_amount': total_amount,
                   'total_amount_with_gst': total_amount_with_gst,
                   'expected_delivery': expected_delivery,
                   'customer_info': customer_info
                   }
        return render(request, 'grocery_management/cart.html',  context)


@login_required
def removeItemFromCart(request, id):
    item = CartItems.objects.get(user_id=request.user.id, id=id)
    userCart = Cart.objects.get(user=request.user.id)
    userCart.total_price = userCart.total_price - item.price
    userCart.save()
    item.delete()
    return redirect('grocery_management:getMyCart')


@login_required
def getitems(request):
    getAllItems = Item.objects.all()
    itemset = ItemSerializer(getAllItems, many=True)
    return render(request, 'grocery_management/products.html', {'Items': getAllItems})


@login_required
def search(request, string):
    itemset = Item.objects.filter(item_name__contains=string)
    Items = []
    for res in itemset:
        Items.append(res)
    return render(request, 'grocery_management/products.html',  {'Items': Items})

@login_required
def homepage(request):
    getAllItems = Item.objects.all()[:6]
    itemset = ItemSerializer(getAllItems, many=True)
    return render(request, 'grocery_management/homepage.html', {'Items': getAllItems})