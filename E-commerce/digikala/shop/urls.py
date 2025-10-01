from django.urls import path
from .views import index ,store , checkout , product

urlpatterns = [
    path('index/' ,index ),
    path('store/' ,store ),
    path('product/' ,product ),
    path('checkout/' ,checkout ),
]
