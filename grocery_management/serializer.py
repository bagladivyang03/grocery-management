from rest_framework import serializers
from .models import *


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRegistration
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
