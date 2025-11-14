from .models import Product

CART_SESSION_ID = 'cart'

class Cart():
    def __init__(self , request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)

        if not cart:
           cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart



    def add(self , product_id , product_price , quantity):
        if product_id not in self.cart:
            self.cart[product_id] = {
            'product_id':product_id,
            'quantity':quantity,
            'price':product_price,
            'TotalPrice':str(int(quantity) * product_price)
        }
        else:
            self.cart[product_id]['quantity'] = int(quantity)
            self.cart[product_id]['TotalPrice'] = str(int(quantity) * product_price)

        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True


    def remove(self,product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True
            self.session[CART_SESSION_ID] = self.cart

    @property
    def product_ids(self):
        return self.cart.keys() 
    @property
    def cart_length(self):
        return len(self.cart) 
    
    @property
    def get_total_price(self):
        total_price = 0
        for item in self.cart.values() :
            total_price += int(item['price']) * int(item['quantity'])

        return  total_price
    
    def __getitem__(self,item):
        return self.cart[item]
    
    # def __iter__(self):
    #     for item in self.cart.values():
    #         yield item
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            item = self.cart[str(product.id)]
            item['product'] = product
            item['product_id'] = product.id 
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    def save(self):
        self.session[CART_SESSION_ID] =self.cart
        self.session.modified = True

    def clear(self):
        self.session[CART_SESSION_ID] ={}
        self.session.modified = True
