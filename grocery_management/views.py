from django.shortcuts import render, redirect
from grocery_management.forms import UserForm, CustomerInfoForm
from .serializer import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
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
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                request.session['user_id'] = request.user.id
                return redirect('/homepage')
            else:
                return HttpResponse("Account doesn't exists")
        else:
            print("Someone tried to d and failed!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("invalid login details supplied!")
    return render(request, 'grocery_management/login.html')


@ login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('grocery_management:login'))


class ItemView(APIView):
    def get(self, request):
        getAllItems = Item.objects.all()
        # itemset = ItemSerializer(getAllItems, many=True)
        return render(request, 'homepage.html', {'Items': getAllItems})
        # return Response(serializer.data)
