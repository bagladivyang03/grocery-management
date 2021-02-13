from django.shortcuts import render, redirect
from grocery_management.forms import UserForm, CustomerInfoForm, ContactUsForm, UpdateInfoForm
from grocery_management.models import CustomerRegistration,Item
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .serializer import CustomerRegistrationSerializer
from . import mailhandler
from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.core import serializers
from datetime import datetime,timedelta
import re


class cartItemsView(APIView):
    def get(self, request):
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
        print(cartItemsDetails)
        lengthofCartItemDetails = len(jsonRes)
        if lengthofCartItemDetails:
            total_amount = jsonRes[lengthofCartItemDetails -
                                   1]['cart_id__total_price']
        else:
            total_amount = 0
        total_amount_with_gst = total_amount+((total_amount*5)/100)
        expected_delivery = str(datetime.today()).split()[0]
        customer_info = CustomerRegistration.objects.get(
            user_id=request.user.id)
        context = {'cartItemsDetails': cartItemsDetails,
                   'lengthofCartItemDetails': lengthofCartItemDetails,
                   'total_amount': total_amount,
                   'total_amount_with_gst': total_amount_with_gst,
                   'expected_delivery': expected_delivery,
                   'customer_info': customer_info
                   }
        return render(request, 'grocery_management/cart.html',  context)


class AboutView(TemplateView):
    template_name = 'grocery_management/about.html'


class HomePageView(TemplateView):
    template_name = 'grocery_management/homepage.html'


class CartView(TemplateView):
    template_name = 'grocery_management/cart.html'


class ProductView(TemplateView):
    template_name = 'grocery_management/products.html'


class ItemView(APIView):
    def get(self, request):
        getAllItems = Item.objects.filter(quantity_available__gt=0)
        itemset = ItemSerializer(getAllItems, many=True)
        return render(request, 'grocery_management/products.html', {'Items': getAllItems})


def check_email(email):
    email_validator_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(email_validator_regex, email):
        return 1
    else:
        return 0


def isPhoneValid(mobile):
    regex = "/[^0-9 +\-]/"
    contact_validator_regex = '^[-+]?[0-9]+$'
    if re.search(contact_validator_regex, mobile):
        if len(mobile) == 10:
            return 1
        else:
            return 0
    else:
        return 0


def validateRegisterForm(request, username, email, password, street, city, pincode, mobile):
    usernameExists = User.objects.filter(username=username).exists()
    emailExists = User.objects.filter(email=email).exists()
    if usernameExists:
        messages.info(
            request, 'A User with the same username already exists', extra_tags='register')
    if not check_email(email):
        messages.info(request, 'Please Provide Valid Email',
                      extra_tags='register')
    if emailExists:
            messages.info(request, 'A User with the same E-Mail already exists',
                      extra_tags='register')
    if not isPhoneValid(mobile):
        messages.info(request, 'Please provide Valid Mobile No',
                      extra_tags='register')
    if len(pincode)!=6:
        messages.info(request, 'Please provide Valid Pincode',
                      extra_tags='register')
    if emailExists or usernameExists or not check_email(email) or not isPhoneValid(mobile) or len(pincode)!=6:
        return 0
    return 1


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        customer_info_form = CustomerInfoForm(data=request.POST)
        if user_form.is_valid() and customer_info_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            street = customer_info_form.cleaned_data['street']
            city = customer_info_form.cleaned_data['city']
            pincode = customer_info_form.cleaned_data['pincode']
            mobile = customer_info_form.cleaned_data['mobile']
            if validateRegisterForm(request, username, email, password, street, city, pincode, mobile):
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                customer_info = customer_info_form.save(commit=False)
                customer_info.user = user
                customer_info.save()
                registered = True
                messages.success(request, 'Account was created')
                return redirect('grocery_management:login')
            else:
                return render(request, 'grocery_management/index.html', {'user_form': user_form, 'customer_info_form': customer_info_form, 'registered': registered})
        # else:
        #     print(user_form)
            # return render(request, 'grocery_management/index.html', {'form': user_form})
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
                    return render(request, 'grocery_management/login.html')
            else:
                messages.info(request, 'Username or Password Incorrect')
                return render(request, 'grocery_management/login.html')
        return render(request, 'grocery_management/login.html', {})


@ login_required
def user_logout(request):
    request.session.flush()
    logout(request)
    return HttpResponseRedirect(reverse('grocery_management:login'))


@ login_required
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
            contact_us_form.save()
            message_sent = True
    else:
        contact_us_form = ContactUsForm()
    return render(request, 'grocery_management/contactus.html', {'contact_us_form': contact_us_form, 'message_sent': message_sent})


@ login_required
def view_profile(request):
    customer_info = CustomerRegistration.objects.get(user_id=request.user.id)
    update_form = UpdateInfoForm(instance=customer_info)
    if request.method == "POST":
        update_form = UpdateInfoForm(request.POST, instance=customer_info)
        if update_form.is_valid():
            update_form.save()
            messages.success(
                request, "Your profile is updated successfully!!", extra_tags='alert-success')
    OrderExists = Order.objects.filter(user=request.user.id).exists()
    if OrderExists:
        userOrder = orderDetails.objects.filter(
            user_id=request.user.id).prefetch_related().values('id', 'quantity', 'order_id', 'order_id__pincode', 'order_id__city', 'order_id__state', 'order_id__contact_no', 'order_id__payment_method', 'order_id__street', 'user_id', 'item__item_name', 'item__image', 'item_id__price', 'item_id__colour_type_id__colour_name', 'item_id__quantity_type_id__variant_name', 'item_id__size_type_id__size_name', 'item_id__description', 'item_id__quantity_available')
        jsonRes = []
        for res in userOrder:
            print(res)
            print()
            if res['item_id__colour_type_id__colour_name'] == None:
                res['item_id__colour_type_id__colour_name'] = 'Not Applicable'
            if res['item_id__quantity_type_id__variant_name'] == None:
                res['item_id__quantity_type_id__variant_name'] = 'Not Applicable'
            if res['item_id__size_type_id__size_name'] == None:
                res['item_id__size_type_id__size_name'] = 'Not Applicable'
            jsonRes.append(res)
        orderItemsDetails = jsonRes
        print(orderItemsDetails)
    if OrderExists:
        context = {'customer_info': customer_info,
                   'update_form': update_form,
                   'orderDetails': orderItemsDetails,
                   'OrderExists': OrderExists
                   }
    else:
        context = {'customer_info': customer_info,
                   'update_form': update_form,
                   'OrderExists': OrderExists
                   }
    return render(request, 'grocery_management/viewprofile.html', context)


@ login_required
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
    print(userCartReference)
    getitem = Item.objects.get(id=id)
    ifItemAlreadyExists = CartItems.objects.filter(item_id=id).exists()
    if not ifItemAlreadyExists:
        itemRef = CartItems()
        itemRef.cart = userCartReference
        itemRef.user = request.user
        itemRef.item = getitem
        itemRef.price = getitem.price
        itemRef.quantity = 1
        itemRef.save()
    else:
        itemRef = CartItems.objects.get(item_id=id)
        itemRef.quantity = itemRef.quantity + 1
        itemRef.save()
    messages.info(request, 'Item Added to Cart', extra_tags='addToCart')
    return redirect('grocery_management:getAllItems')


@ login_required
def removeItemFromCart(request, id):
    item = CartItems.objects.get(user_id=request.user.id, id=id)
    print(item.quantity)
    print()
    userCart = Cart.objects.get(user=request.user.id)
    print(userCart.total_price)
    userCart.total_price = userCart.total_price - (item.quantity*item.price)
    print(userCart.total_price)
    userCart.save()
    print(userCart)
    item.delete()
    # if(item.quantity > 1):
    #     userCart.total_price = userCart.total_price - item.price
    #     print(userCart.total_price)
    #     userCart.save()
    #     item.quantity = item.quantity - 1;
    #     item.save()
    # else:   
    #     print(userCart.total_price)
    #     userCart.total_price = userCart.total_price - item.price
    #     print(userCart.total_price)
    #     userCart.save()
    #     print(userCart)
    #     item.delete()
    return redirect('grocery_management:getMyCart')


@ login_required
def getitems(request):
    getAllItems = Item.objects.filter(Item__quantity_available__gt=0)
    print(getAllItems)
    itemset = ItemSerializer(getAllItems, many=True)
    return render(request, 'grocery_management/products.html', {'Items': getAllItems})


@ login_required
def search(request):
    string = request.POST.get('searchString')
    if string:
        itemset = Item.objects.filter(item_name__contains=string)
        Items = []
        for res in itemset:
            Items.append(res)
        return render(request, 'grocery_management/products.html',  {'Items': Items})
    return render(request, 'grocery_management/products.html',  {})


@ login_required
def homepage(request):
    getAllItems = Item.objects.filter(quantity_available__gt=0)[:6]
    itemset = ItemSerializer(getAllItems, many=True)
    return render(request, 'grocery_management/homepage.html', {'Items': getAllItems})


@ login_required
def checkout(request):
    customer_info = CustomerRegistration.objects.get(
        user_id=request.user.id)
    if not request.POST.get('username'):
        messages.info(request, 'Please Enter Username', extra_tags='checkout')
    if not request.POST.get('email'):
        messages.info(request, 'Please Enter Email', extra_tags='checkout')
    if not request.POST.get('pincode'):
        messages.info(request, 'Please Enter Pincode', extra_tags='checkout')
    if not request.POST.get('street'):
        messages.info(request, 'Please Enter Street', extra_tags='checkout')
    if not request.POST.get('city'):
        messages.info(request, 'Please Enter City', extra_tags='checkout')
    if not request.POST.get('mobile'):
        messages.info(request, 'Please Enter Mobile', extra_tags='checkout')
    if not request.POST.get('state'):
        messages.info(request, 'Please Enter State', extra_tags='checkout')
    if not request.POST.get('username') or not request.POST.get('email') or not request.POST.get('pincode') or not request.POST.get('street') or not request.POST.get('city') or not request.POST.get('mobile') or not request.POST.get('state') or not request.POST.get('state'):
        return render(request, 'grocery_management/cart.html',{'customer_info':customer_info})
    OrderExists = Order.objects.filter(user=request.user.id).exists()
    userCart = CartItems.objects.filter(
        user_id=request.user.id).prefetch_related().values('id', 'price', 'quantity', 'cart_id', 'cart_id__total_price', 'user_id', 'item_id', 'item__item_name', 'item__image', 'item_id__price', 'item_id__colour_type_id__colour_name', 'item_id__quantity_type_id__variant_name', 'item_id__size_type_id__size_name', 'item_id__description', 'item_id__quantity_available')
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
    ordered_date = str(datetime.today()).split()[0]
    if not OrderExists:
        orderObj = Order()
        orderObj.user = request.user
        orderObj.ordered_date = ordered_date
        orderObj.pincode = request.POST.get('pincode')
        orderObj.street = request.POST.get('street')
        orderObj.city = request.POST.get('city')
        orderObj.contact_no = request.POST.get('mobile')
        orderObj.state = request.POST.get('state')
        orderObj.country = request.POST.get('country')
        orderObj.save()
    getOrderObj = Order.objects.get(user=request.user.id)
    for item in cartItemsDetails:
        print(item)
        print()
        item_up = Item.objects.get(
        item_name = item['item__item_name'],
        )
        item_up.quantity_available = item_up.quantity_available - item['quantity']
        item_up.save()
        getitem = Item.objects.get(id=item['item_id'])
        orderDetailsObj = orderDetails()
        orderDetailsObj.user = request.user
        orderDetailsObj.order = getOrderObj
        orderDetailsObj.item = getitem
        orderDetailsObj.quantity = item['quantity']
        orderDetailsObj.save()
    Cart.objects.filter(user_id=request.user.id).delete()
    context = {}
    return render(request, 'grocery_management/cart.html',  context)
