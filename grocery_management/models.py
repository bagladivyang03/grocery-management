from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class CustomerRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    mobile = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.user.username


class MessageUsInfo(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)


class QuantityVariant(models.Model):
    variant_name = models.CharField(max_length=10)

    def __str__(self):
        return self.variant_name


class ColorVariant(models.Model):
    colour_name = models.CharField(max_length=30)
    colour_code = models.CharField(max_length=30)

    def __str__(self):
        return self.colour_name


class SizeVariant(models.Model):
    size_name = models.CharField(max_length=30)

    def __str__(self):
        return self.size_name


class Item(models.Model):
    item_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='static/products')
    price = models.CharField(max_length=15)
    description = models.TextField()
    quantity_available = models.IntegerField(default=10)
    quantity_type = models.ForeignKey(
        QuantityVariant, blank=True, null=True, on_delete=models.PROTECT)
    colour_type = models.ForeignKey(
        ColorVariant, blank=True, null=True, on_delete=models.PROTECT)
    size_type = models.ForeignKey(SizeVariant, blank=True,
                                  null=True, on_delete=models.PROTECT)

    class Meta:
        pass

    def __str__(self):
        return self.item_name


class ItemImages(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='static/products')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.username)+" "+str(self.total_price)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user.username)+" "+str(self.item.item_name)


@receiver(pre_save, sender=CartItems)
def recalculate_total_price(sender, **kwargs):
    cart_items = kwargs['instances']
    price_of_item = Item.objects.get(id=cart_items.item.id)
    cart_items.price = cart_items.quantity * float(price_of_item.price)
    total_cart_item = CartItems.objects.filter(user=cart_items.user)
    cart = Cart.objects.get(id=cart_items.cart.id)
    cart.total_price = cart_items.price
    cart.save()
