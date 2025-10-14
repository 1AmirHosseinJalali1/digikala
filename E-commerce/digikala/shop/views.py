from django.shortcuts import  render , get_object_or_404 , redirect
from .models import Product
from django.http import Http404
from django.views.decorators.http import require_POST
from django.urls import reverse
# Create your views here.

def index(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request , 'index.html',context)

def store(request):
    category = request.GET.get('category')
    if category is not None:
        products = Product.objects.filter(category__title=category)
        context = {
        'products':products
    }
        return render(request , 'store.html',context)
    

    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request , 'store.html',context)

def checkout(request):
    return render(request , 'checkout.html')

def detail(request,id=int,title=str):

    
    product = get_object_or_404(Product,id=id)
    context = {
            'product':product
        }
    
    return render(request , 'detail.html',context)


@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')


    product = get_object_or_404(Product , id = product_id)

    cart = request.session.get('cart')

    if not cart :
        cart = request.session['cart'] = {}
    if product_id in cart:
        cart[product_id]['quantity'] = int(quantity)
        cart[product_id]['TotalPrice'] = str(int(quantity) * product.price)
    
    else:
        cart[product_id] = {
            'quantity': int(quantity),
            'price': product.price,
            'TotalPrice' : str(int(quantity) * product.price)
        }
    
            
    request.session.modified = True
    request.session['cart'] = cart

    return redirect(reverse('shop:cart_detail')  )


def cart_detail(request):
    cart = request.session.get('cart')
    if cart:
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['TotalPrice'] = int(item['price']) * item['quantity']

        return render(request , 'cart_detail.html', {'cart':cart})
    return render(request , 'cart_detail.html')

def remove_from_cart(request,product_id):
    product = get_object_or_404(Product , id = product_id)
    
    cart = request.session.get('cart',{})
    pid = str(product_id)

    if pid in cart:
            del cart[pid]
            request.session.modified = True
    
    
    return redirect(reverse('shop:cart_detail'))


