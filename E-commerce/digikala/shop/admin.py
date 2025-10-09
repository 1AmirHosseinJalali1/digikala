from django.contrib import admin
from . import models
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title']
    list_filter  = ['title']
    search_fields = ['title']

    def delete_queryset(self, request, queryset):
        for category in queryset:
            category.delete()

class ProductAdmin(admin.ModelAdmin):
    list_display  = ['id','title','price','quantity','status']
    search_fields = ['title']
    list_filter   = ['status']

    def delete_queryset(self, request, queryset):
        for product in queryset:
            product.delete()


class CartAdmin(admin.ModelAdmin):
    list_display = ['id','product','user','quantity']

    def delete_queryset(self,request,queryset):
        for cart in queryset:
             cart.delete()


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','total_price','user','status']
    list_filter  = ['status']

    def delete_queryset(self,request,queryset):
        for order in queryset:
             order.delete()

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id','product','order','quantity','price','order_id']
  

    def delete_queryset(self,request,queryset):
        for order in queryset:
             order.delete()





admin.site.register(models.Cart,CartAdmin)
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.OrderProduct,OrderProductAdmin)
admin.site.register(models.Order,OrderAdmin)
admin.site.register(models.Category,CategoryAdmin)

