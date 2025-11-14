from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Product, Order
from django.http import Http404
from django.views.decorators.http import require_POST
from django.urls import reverse
from .cart import Cart
from django.contrib.auth.decorators import login_required
from .models import OrderProduct
from accounts.models import Profile, Province, City
from .forms import OrderForm
from django.conf import settings
from django.shortcuts import redirect
import json
import requests
# import requests

# Create your views here.


def index(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'index.html', context)


def store(request):
    category = request.GET.get('category')

    if category:
        products = Product.objects.filter(category__title=category)

    else:
        products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'store.html', context)


@login_required
def checkout(request):
    try:
        Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect(reverse('accounts:edit_profile') + '?next=' + reverse('shop:checkout'))

    cart = Cart(request)

    if request.method == 'POST':
        different_address = request.POST.get('different_address')
        order = None

        if different_address:
            order_form = OrderForm(request.POST)
            print("🧾 فرم ارسال شد، خطاهای احتمالی:", order_form.errors)
            if not order_form.is_valid():
                context = {'provinces': Province.objects.all(), 'form_errors': order_form.errors}
                return render(request, 'checkout.html', context)

            order = Order.objects.create(
                user=request.user,
                total_price=cart.get_total_price,
                note=request.POST.get('note', ''),
                different_address=True,
                first_name=order_form.cleaned_data['first_name'],
                last_name=order_form.cleaned_data['last_name'],
                mobile=order_form.cleaned_data['mobile'],
                postal_code=order_form.cleaned_data['postal_code'],
                address=order_form.cleaned_data['address'],
                city_id=order_form.cleaned_data['city'],
            )
        else:
            order = Order.objects.create(
                user=request.user,
                total_price=cart.get_total_price,
                different_address=False,
                note=request.POST.get('note', ''),
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                mobile=request.user.mobile,
                postal_code=request.user.profile.postal_code,
                address=request.user.profile.address,
                city=request.user.profile.city,
            )

        # ذخیره محصولات سفارش
        for item in cart:
            OrderProduct.objects.create(
                order=order,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item['price']
            )

        # cart.clear()
        return redirect(reverse('shop:to_bank', args=[order.id]))

    # حالت GET
    context = {
        'provinces': Province.objects.all(),
    }
    return render(request, 'checkout.html', context)


@login_required
def to_bank(request, order_id):
    cart = Cart(request)
    order = get_object_or_404(
        Order, id=order_id, user=request.user, status__isnull=True)

    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": order.total_price,
        "description": f"Order #{order_id}",
        "callback_url": settings.ZARINPAL_CALLBACK_URL,
        "metadata": {"order_id": str(order.id), "email": request.user.email}
    }
    print("زرین‌پال request to_bank:", data)

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            "https://sandbox.zarinpal.com/pg/v4/payment/request.json",
            data=json.dumps(data),
            headers=headers,
            timeout=10
        )
    except requests.exceptions.Timeout:
        return render(request, "to_bank.html", {"error": "Timeout error"})
    except requests.exceptions.ConnectionError:
        return render(request, "to_bank.html", {"error": "Connection error"})

    res_json = response.json()
    data = res_json.get("data", {})
    print("زرین‌پال verify response:", res_json)
    if response.status_code != 200:
        return render(request, "to_bank.html", {"error": f"HTTP {response.status_code}"})
    if data.get("code") != 100:
        
        return render(request, "to_bank.html", {"error": data.get("message", "Error")})

    authority = data["authority"]
    order.zarinpal_authority = authority
    order.status = False
    order.save()
    cart.clear()
    # ریدایرکت به درگاه پرداخت
    return redirect(f"https://sandbox.zarinpal.com/pg/StartPay/{authority}")


def verify(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if not authority:
        return render(request, "verify.html", {"success": False, "error": "کد تراکنش موجود نیست."})

    order = Order.objects.filter(zarinpal_authority=authority).first()
    if not order:
        return render(request, "verify.html", {"success": False, "error": "سفارشی با این تراکنش پیدا نشد."})

    if status != 'OK':
        return render(request, "verify.html", {"success": False, "error": "پرداخت لغو شد یا انجام نشد."})

    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": order.total_price,
        "authority": authority
    }
    print("زرین‌پال request to_bank:", data)

    headers = {"Content-Type": "application/json"}
    response = requests.post(
        settings.ZARINPAL_VERIFY_URL,
        data=json.dumps(data),
        headers=headers,
        timeout=10
    )

    print("زرین‌پال verify response:", response.text)  # 🔹 مهم برای debug

    res_json = response.json()
    data = res_json.get("data", {})

    if data.get("code") == 100:
        order.zarinpal_ref_id = data["ref_id"]
        order.status = True
        order.save()
        return render(request, "verify.html", {"success": True, "ref_id": data["ref_id"], "order": order})
    else:
        return render(request, "verify.html", {"success": False, "error": data})


def detail(request, id=int, title=str):

    product = get_object_or_404(Product, id=id)
    context = {
        'product': product
    }

    return render(request, 'detail.html', context)

@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    product = get_object_or_404(Product, id=product_id)

    cart = Cart(request)

    cart.add(product_id, product.price, quantity)

    return redirect(reverse('shop:cart_detail'))


def remove_from_cart(request, product_id):

    cart = Cart(request)
    cart.remove(str(product_id))
    return redirect(reverse('shop:cart_detail'))
    # cart = request.session.get('cart')
    # pid = str(product_id)

    # if pid in cart:
    #         del cart[pid]
    #         request.session.modified = True


def cart_detail(request):

    return render(request, 'cart_detail.html')

