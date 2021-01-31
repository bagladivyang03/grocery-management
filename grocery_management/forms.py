from django import forms
from django.contrib.auth.models import User
from grocery_management.models import CustomerRegistration, MessageUsInfo


class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control bg-white border-left-0 border-md','placeholder':'Password'}))

    class Meta():
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-white border-left-0 border-md', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-white border-left-0 border-md', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control bg-white border-left-0 border-md', 'placeholder': 'Password'}),
        }


class CustomerInfoForm(forms.ModelForm):
    class Meta():
        model = CustomerRegistration
        fields = ('street', 'city', 'pincode', 'mobile')
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control bg-white border-left-0 border-md', 'placeholder': 'Street'}),
            'city': forms.TextInput(attrs={'class': 'form-control bg-white border-left-0 border-md', 'placeholder': 'City'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control bg-white border-left-0 border-md', 'placeholder': 'Pincode'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control bg-white border-left-0 border-md', 'placeholder': 'Mobile No.'}),
        }


class ContactUsForm(forms.ModelForm):
    class Meta():
        model = MessageUsInfo
        fields = ('fullname', 'email', 'subject', 'message')
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'E-Mail Address'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'id': 'subject', 'placeholder': 'Subject'}),
            'message': forms.TextInput(attrs={'rows': '6', 'class': 'form-control', 'id': 'message', 'placeholder': 'Your Message'}),
        }


class UpdateInfoForm(forms.ModelForm):
    class Meta():
        model = CustomerRegistration
        fields = ('street', 'city', 'pincode', 'mobile')
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control no-border'}),
            'city': forms.TextInput(attrs={'class': 'form-control no-border'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control no-border'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control no-border'}),
        }
