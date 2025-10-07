from django.db import models
from django.contrib.auth.models import AbstractUser ,UserManager
from django.utils.translation import gettext_lazy
# Create your models here.

class soft_user_manager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted = False)




class User(AbstractUser):
    mobile = models.CharField(max_length=11,unique=True)
    email = models.EmailField(gettext_lazy('email address'),unique=True)    
    deleted = models.BooleanField(default=False,editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self , using=None , keep_parents= False):
        self.deleted = True
        self.save()