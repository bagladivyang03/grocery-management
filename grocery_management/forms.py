from django import forms
from django.contrib.auth.models import User
from grocery_management.models import CustomerRegistration,MessageUsInfo

class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control bg-white border-left-0 border-md','placeholder':'Password'}))

    class Meta():
        model = User
        fields = ('username','email','password')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control bg-white border-left-0 border-md','placeholder':'Username'}),
            'email':forms.EmailInput(attrs={'class':'form-control bg-white border-left-0 border-md','placeholder':'Email'}),
            'password':forms.PasswordInput(attrs={'class':'form-control bg-white border-left-0 border-md','placeholder':'Password'}),
        }

    def clean(self):
        
        super(UserForm, self).clean()
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if len(username) < 2:
            self._errors['username'] = self.error_class([
                'Username is required'])
        if len(email) ==0:
            self._errors['email'] = self.error_class([
                'Email is required'])
        if len(password) ==0:
            self._errors['password'] = self.error_class([
                'Paaword is required'])

        return self.cleaned_data


class CustomerInfoForm(forms.ModelForm):
    class Meta():
        model = CustomerRegistration
        fields = ('street','city','pincode','mobile')
        widgets = {
            'street':forms.TextInput(attrs={'class':'form-control bg-white border-left-0 border-md','placeholder':'Street'}),
            'city':forms.TextInput(attrs={'class':'form-control bg-white border-left-0 border-md','placeholder':'City'}),
            'pincode':forms.TextInput(attrs={'class':'form-control bg-white border-left-0 border-md','placeholder':'Pincode'}),
            'mobile':forms.TextInput(attrs={'class':'form-control bg-white border-left-0 border-md','placeholder':'Mobile No.'}),
        }


    def clean(self):
         
        super(CustomerInfoForm, self).clean()
        street = self.cleaned_data.get('username')
        city = self.cleaned_data.get('email')
        pincode = self.cleaned_data.get('password')

        if len(street) < 5:
            self._errors['street'] = self.error_class([
                'street is required'])
        if len(city) ==0:
            self._errors['city'] = self.error_class([
                'Email is required'])
        if len(pincode) ==0:
            self._errors['pincode'] = self.error_class([
                'Paaword is required'])

        return self.cleaned_data


class UpdateInfoForm(forms.ModelForm):
    class Meta():
        model = CustomerRegistration
        fields = ('street','city','pincode','mobile')
        widgets = {
            'street':forms.TextInput(attrs={'class':'form-control no-border'}),
            'city':forms.TextInput(attrs={'class':'form-control no-border'}),
            'pincode':forms.TextInput(attrs={'class':'form-control no-border'}),
            'mobile':forms.TextInput(attrs={'class':'form-control no-border'}),
        }

    
class ContactUsForm(forms.ModelForm):
    class Meta():
        model = MessageUsInfo
        fields = ('fullname','email','subject','message')
        widgets = {
            'fullname': forms.TextInput(attrs={'class':'form-control' ,'id':'name' ,'placeholder':'Full Name'}),
            'email': forms.EmailInput(attrs={'class':'form-control' ,'id':'email', 'placeholder':'E-Mail Address'}),
            'subject': forms.TextInput(attrs={'class':'form-control' ,'id':'subject', 'placeholder':'Subject'}),
            'message': forms.TextInput(attrs={'rows':'6', 'class':'form-control' ,'id':'message', 'placeholder':'Your Message'}),
        }