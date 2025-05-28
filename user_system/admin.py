from django.contrib import admin
from user_system.models import (
    Customer,
    Seller,
    Shopping_Cart,
    Order,
)

# Register your models here.

class SellerAdmin(admin.ModelAdmin):
    list_display = (
        'user_ID',
        'user_mail',
        'user_name',
        'user_password',
        'get_products',
        'rating'
    )

    def get_products(self, obj):
        return "、".join([f"{p.name}, ${p.price}, {p.quantity}個" for p in obj.products.all()])
    get_products.short_description = 'Products'

class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'user_ID',
        'user_mail',
        'user_name',
        'user_password',
        'address'
    )

class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'get_user_ID',
        'get_product',
        'quantity'
    )

    def get_user_ID(self, obj):
        return obj.user_ID.user_ID
    get_user_ID.short_description = 'user_ID'

    def get_product(self, obj):
        return obj.product.name
    get_product.short_description = 'Products'

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_ID',
        'products',
        'get_customer_ID',
        'get_seller_ID',
        'date'
    )
    
    def get_customer_ID(self, obj):
        return (obj.customer_ID).user_ID
    
    def get_seller_ID(self, obj):
        return (obj.seller_ID).user_ID
    
    get_customer_ID.short_description = 'Customer_ID' 
    get_seller_ID.short_description = 'Seller_ID'    


admin.site.register(Seller, SellerAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Shopping_Cart, ShoppingCartAdmin)
admin.site.register(Order, OrderAdmin)