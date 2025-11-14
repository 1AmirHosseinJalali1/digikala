from django.shortcuts import render ,redirect 
from django.http import HttpResponse ,JsonResponse 
from .models import City , User
from django.contrib.auth import authenticate , login ,logout
from accounts.forms import LoginForm , RegisterForm , EmailLoginForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes ,force_str 
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def edit_profile(request):
    return HttpResponse('<h1>Edit Profile</h1>')


def get_cities(request):
    province_id = request.GET.get('province_id')
    if not province_id:
        return JsonResponse({"error":'province id is not valid'})
    cities = City.objects.filter(province_id = province_id).values('id','title')
    return JsonResponse(list(cities) , safe=False)

def login_view(request):
    next_page = request.GET.get('next')

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(next_page)  # اگر next نبود، برو به صفحه اصلی
        else:
            form.add_error(None, "نام کاربری یا رمز عبور اشتباه است.")
            messages.error(request, 'Invalid username or password','danger')
    return render(request, 'login.html', {'form': form})
# def login(request):
#     next_page = request.GET.get('next')
#     if request.method == 'GET':

#         form = LoginForm()
#         return render(request , 'login.html' , {'form':form})
    
#     form = LoginForm(request.POST)
#     if form.is_valid():
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user = authenticate(request,username=username , password = password)
#         if user is not None:
#             django_login(request , user)
#             return redirect(next_page)
#     else:
#         return render(request , 'login.html' , {'form':form})


def logout_view(request):
    logout(request)
    return redirect(reverse('shop:index'))

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request,'register.html',{'form':form})
        
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site     = get_current_site(request)
        token            = default_token_generator.make_token(user)
        encoded_user_id  = urlsafe_base64_encode(force_bytes(user.id))
        activation_path  = reverse('accounts:active_email',args=[encoded_user_id ,token])
        activation_url   = f'http://{current_site}{activation_path}'




        send_activation_code(activation_url,form.cleaned_data['email'])

        messages.info(request,'see your activation code')
        return redirect('accounts:login')
    
    form = RegisterForm()
    return render(request,'register.html',{'form':form})



def send_activation_code(activation_url ,email_address):

    send_mail(
    subject="Activate your account",
    message=f"please click on the link below to activate user account.{activation_url}",
    from_email="admin@admin.com",
    recipient_list=[email_address],
    )


def active_email(request , encoded_user_id , token):
    user_id = force_str(urlsafe_base64_decode(encoded_user_id))
    try:
        user = User.objects.get(id = user_id , is_active = False)
    except (ValueError , User.DoesNotExist):
        return HttpResponse('<h1>error , your request is invalid.</h1>')

    if not default_token_generator.check_token(user,token):
        return HttpResponse('<h1>Error , your activation link is invalid.</h1>')
    
    user.is_active = True
    user.save()
    return HttpResponse(f'<h1>your account succifully activated</h1>')


def mobile_login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        if mobile:
            request.session['mobile'] = mobile
            if cache.get(mobile):
                return redirect(reverse('accounts:verify_otp'))
            send_otp(mobile)
            return redirect(reverse('accounts:verify_otp'))
    return render(request , 'mobile_login.html')


def send_otp(mobile):
    import random
    

    otp = random.randint(1000,9999)
    cache.set(mobile, otp ,60 )
    #send otp with sms service
    print(f"otp for {mobile}: {otp}")

def verify_otp(request):
    mobile = request.session.get('mobile')
    if not mobile:
        return redirect(reverse('accounts:mobile_login'))
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        
        # اطمینان از اینکه OTP عدد صحیح است
        try:
            otp = int(otp)
        except ValueError:
            messages.error(request, 'OTP must be a valid number', 'danger')
            return render(request, 'verify_otp.html')

        # دریافت OTP ذخیره شده در کش
        cached_otp = cache.get(mobile)

        # اگر OTP موجود نیست یا منقضی شده
        if cached_otp is None:
            messages.error(request, 'OTP has expired or is invalid', 'danger')
            return render(request, 'verify_otp.html')

        # مقایسه OTP واردشده با کش
        if cached_otp != otp:
            messages.error(request, 'Invalid OTP code', 'danger')
            return render(request, 'verify_otp.html')
        
        # کاربر را می‌سازیم اگر وجود نداشته باشد
        user, created = User.objects.get_or_create(
            mobile=mobile,
            defaults={'username': mobile, 'email': f'{mobile}@gmail.com'}
        )

        # بررسی وضعیت حساب کاربر
        if not user.is_active:
            messages.error(request, 'Your account is inactive', 'danger')
            return render(request, 'verify_otp.html')

        # احراز هویت کاربر
        user = authenticate(mobile=mobile)
        if user is not None:
            login(request, user)
            cache.delete(mobile)  # حذف OTP از کش بعد از موفقیت
            return redirect(reverse('shop:index'))
        else:
        # در صورتی که کاربر شناسایی نشد
            messages.error(request, 'Account does not exist or invalid credentials', 'danger')
        
    return render(request, 'verify_otp.html')

# def verify_otp(request):
#     mobile = request.session.get('mobile')
#     if not mobile:
#         return redirect(reverse('accounts:mobile_login'))
    
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         cached_otp = cache.get(mobile)
#         if cached_otp and cached_otp == int(otp) :
            
#             User.objects.get_or_create(
#                 mobile=mobile,
#                 defaults={
#                     'username':mobile,
#                     'email':f'{mobile}@gmail.com'
#                 }
#                 )
#             user = authenticate(mobile = mobile)
#             if user is not None:
#                 login(request,user)
#                 cache.delete(mobile)
#                 return redirect(reverse('shop:index'))
        
#         messages.error(request, 'your otp code is invalid or account is inactive','danger')
        
#     return render(request , 'verify_otp.html')
        

def resend_otp(request):
    mobile = request.session.get('mobile')
    if not mobile:
        return redirect(reverse('accounts:mobile_login'))
    
    
    if cache.get(mobile):
        return redirect(reverse('accounts:verify_otp'))
    
    send_otp(mobile)
    return redirect(reverse('accounts:verify_otp'))

def email_login(request):
    
    if request.method == 'GET':
        form = EmailLoginForm()
        return render(request, 'login.html', {'form': form})

    form = EmailLoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('shop:index'))  # اگر next نبود، برو به صفحه اصلی
        else:
            form.add_error(None, "نام کاربری یا رمز عبور اشتباه است.")
            messages.error(request, 'Invalid email or password','danger')
    return render(request, 'login.html', {'form': form})