from .cart import Cart
from .models import Product


def cart_context(request):
    cart = Cart(request)
    if cart :
        product_ids = cart.product_ids
        product_list = Product.objects.filter(id__in = product_ids)

        for product in product_list:
            cart[str(product.id)]['product'] = product
        cart_length = 0
        FinalPrice = 0
        for item in cart:
            FinalPrice += int(item['TotalPrice'])
            cart_length += int(item['quantity'])
        return {'cart':cart , 'FinalPrice':FinalPrice , 'cart_length':cart_length}