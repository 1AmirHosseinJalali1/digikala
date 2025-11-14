from django.contrib.auth.backends import ModelBackend
from accounts.models import User

from django.contrib.auth.backends import ModelBackend
from accounts.models import User

# class EmailBackend(ModelBackend):
#     """
#     احراز هویت بر اساس ایمیل از مدل AUTH_USER_MODEL
#     """

#     def authenticate(self, request, username=None, password=None, **kwargs):
#         email = kwargs.get('email')
        
#         if email is None or password is None:
#             return None  # اگر ایمیل یا رمز عبور وارد نشده باشد، بازگشت None
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             # به منظور کاهش تفاوت زمانی بین کاربر موجود و کاربر غیرموجود،
#             # هش کردن پسورد به صورت پیش‌فرض انجام می‌شود (#20760).
#             User().set_password(password)
#         else:
#             # اگر رمز عبور صحیح بود و کاربر می‌تواند وارد سیستم شود، کاربر را برمی‌گردانیم
#             if user.check_password(password) and self.user_can_authenticate(user):
#                 return user

# class MobileBackend(ModelBackend):
#     """
#     احراز هویت بر اساس شماره موبایل از مدل AUTH_USER_MODEL
#     """

#     def authenticate(self, request, username=None, password=None, **kwargs):
#         mobile = kwargs.get('mobile')
        
#         if mobile is None or password is None:
#             return None  # اگر شماره موبایل یا رمز عبور وارد نشده باشد، بازگشت None
#         try:
#             user = User.objects.get(mobile=mobile)
#         except User.DoesNotExist:
#             # به منظور کاهش تفاوت زمانی بین کاربر موجود و کاربر غیرموجود،
#             # هش کردن پسورد به صورت پیش‌فرض انجام می‌شود (#20760).
#             User().set_password(password)
#         else:
#             # اگر رمز عبور صحیح بود و کاربر می‌تواند وارد سیستم شود، کاربر را برمی‌گردانیم
#             if user.check_password(password) and self.user_can_authenticate(user):
#                 return user


class EmailBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email')
        
        if email is None or password is None:
            return
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            

class MobileBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        mobile = kwargs.get('mobile')
        
        if mobile is None :
            return
        try:
            user = User.objects.get(mobile = mobile)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(mobile)
        else:
            if self.user_can_authenticate(user):
                return user