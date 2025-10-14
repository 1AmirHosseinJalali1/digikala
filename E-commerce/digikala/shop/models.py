from django.db import models
from django.conf import settings
# Create your models here.

# class User(models.Model):
#     mobile = models.CharField(max_length=11)
class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted = False)


class BaseModel(models.Model):
    deleted = models.BooleanField(default=False,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseModelManager()

    class Meta:
        abstract = True

    def delete(self , using=None , keep_parents= False):
        self.deleted = True
        self.save()

class Category(BaseModel):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Product(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='image/product')
    quantity = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL ,null=True , blank=True)
    
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("shop:detail", kwargs={'id':self.id, 'title':self.title})

class Cart(BaseModel):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class Order(BaseModel):
    total_price = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    status = models.BooleanField(null=True)

class OrderProduct(BaseModel):
    product = models.ForeignKey(Product , on_delete=models.SET_DEFAULT , default=None , null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()


class PaymentLog(BaseModel):
    amount = models.IntegerField()
    user_id = models.PositiveIntegerField()
    order_id = models.PositiveIntegerField()
    status = models.CharField(max_length=100)
    error_code = models.CharField(max_length=200)


