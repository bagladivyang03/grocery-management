from django.shortcuts import render,redirect
from grocery_management.forms import UserForm, CustomerInfoForm, ContactUsForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.mail import send_mail
# Create your views here.

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        customer_info_form = CustomerInfoForm(data = request.POST)

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

    return render(request,'grocery_management/index.html',{'user_form' : user_form,'customer_info_form' : customer_info_form,'registered' : registered})


def user_login(request):
    if request.method=='POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                (request,user)
                return render(request,"grocery_management/homepage.html")
            else:
                return HttpResponse("Account doesn't exists")
        else:
            print("Someone tried to d and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")
    return render(request,'grocery_management/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('grocery_management:login'))


class AboutView(TemplateView):
    template_name = 'grocery_management/about.html'


class HomePageView(TemplateView):
    template_name = 'grocery_management/homepage.html'

# class ContactUsView(TemplateView):
#     template_name = 'grocery_management/contactus.html'


def contact_us(request):

    message_sent = False;
    if request.method == "POST":
        contact_us_form = ContactUsForm(data = request.POST)

        if contact_us_form.is_valid():

            sender_name = contact_us_form.cleaned_data['fullname']
            sender_email = contact_us_form.cleaned_data['email']

            message = "{0} has sent you a new message:\n\n{1}".format(sender_name,contact_us_form.cleaned_data['subject'], contact_us_form.cleaned_data['message'])
            send_mail('New Enquiry', message, sender_email, ['bagladivyang03@gmail.com'])
            contact_us_form.save()
            message_sent = True
    else:
        contact_us_form = ContactUsForm()
    
    return render(request,'grocery_management/contactus.html',{'contact_us_form' : contact_us_form,'message_sent':message_sent})
            