from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
# Create your models here.

# model representation of the canteen meal
User = get_user_model()
class MenuItem(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()
    photo = models.ImageField(upload_to='Customers/image')
    is_available = models.BooleanField(default=True)
    category = models.ManyToManyField("Category", related_name='item')
    user = models.ManyToManyField(User, related_name='userOrder', blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# model representation for the contact form

class Contact(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    Email = models.EmailField()
    subject = models.CharField(max_length=50, null=True)
    message = models.TextField()

    def __str__(self):
        return self.email


# model representation of the order

class Order(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='order_user')
    price = models.DecimalField(max_digits=7, decimal_places=2,default=False)
    # menu_item = models.ManyToManyField(MenuItem, related_name='order', blank=True)
    Date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, null=True, blank=True)
    menu_item = models.ForeignKey(MenuItem, related_name="menu_item", on_delete=models.CASCADE, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    # user = models.ManyToManyField(User, related_name='userOrder', blank=True)

    # name = models.CharField(max_length=50, blank=True)
    # email = models.CharField(max_length=50, blank=True)
    # street = models.CharField(max_length=50, blank=True)
    # postcode = models.CharField(max_length=15, blank=True)
    # city = models.CharField(max_length=50, blank=True)


    def __str__(self):
        return str(self.Date_created)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     quantity = models.PositiveIntegerField(default=1)
#
#     def __str__(self):
#         return str(self.id)
