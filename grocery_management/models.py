from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class CustomerRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    street =  models.CharField(max_length=50)
    city =  models.CharField(max_length=50)
    pincode =  models.CharField(max_length=6)
    mobile = models.CharField(max_length = 10)

    def __str__(self):
        return self.user.username


class MessageUsInfo(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)
    
    



