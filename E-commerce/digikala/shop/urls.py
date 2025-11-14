from django.urls import path
from .views import verify,index ,store , checkout , detail ,add_to_cart ,cart_detail ,remove_from_cart,to_bank


app_name = 'shop'


urlpatterns = [
    path('index/' ,index,name='index' ),
    path('store/' ,store ,name='store'),
    path('<int:id>/<str:title>/' ,detail ,name='detail'),
    path('checkout/' ,checkout,name='checkout' ),
    path('to-bank/<int:order_id>/' ,to_bank,name='to_bank' ),
    path('verify/' ,verify,name='verify' ),
    path('add-to-cart' , add_to_cart , name='add_to_cart'),
    path('cart' , cart_detail , name='cart_detail'),
    path('cart/remove/<int:product_id>/' , remove_from_cart , name='remove_from_cart'),
    
]
