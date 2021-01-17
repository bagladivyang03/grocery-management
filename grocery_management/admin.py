from django.contrib import admin
from grocery_management.models import CustomerRegistration, MessageUsInfo, QuantityVariant, ColorVariant, SizeVariant, ItemImages, Item, Cart, CartItems
# Register your models here.
admin.site.register(CustomerRegistration)
admin.site.register(MessageUsInfo)
admin.site.register(QuantityVariant)
admin.site.register(ColorVariant)
admin.site.register(SizeVariant)
admin.site.register(Item)
admin.site.register(ItemImages)
admin.site.register(CartItems)
admin.site.register(Cart)
