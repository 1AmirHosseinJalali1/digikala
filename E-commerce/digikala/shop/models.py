from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class User(models.Model):
#     mobile = models.CharField(max_length=11)

class Category(models.Model):
    title = models.CharField(max_length=100)
    

class Product(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    price = models.IntegerField()
    image = models.ImageField()
    quantity = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Order(models.Model):
    total_price = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class PaymentLog(models.Model):
    amount = models.IntegerField()
    user_id = models.PositiveIntegerField()
    order_id = models.PositiveIntegerField()
    status = models.CharField(max_length=100)
    error_code = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


