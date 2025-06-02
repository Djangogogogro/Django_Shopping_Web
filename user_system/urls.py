from django.urls import path
from user_system.views import (
    Register_View,
    Login_View,
    logout_view,
    Add_To_Cart_View,
    Shopping_Cart_View,
    My_Products_View,
    Add_Products,
    Buy_View,
    Edit_Product,
)

urlpatterns = [
    path("new/<str:model_type>", Register_View.as_view(), name="New User"),
    path("login/<str:model_type>", Login_View.as_view(), name="Login"),
    path('logout/', logout_view, name='logout'),
    path('product/<int:pk>/add/', Add_To_Cart_View.as_view(), name='Add To Cart'),
    path('ShoppingCart', Shopping_Cart_View.as_view(), name='Shopping Cart'),
    path('ShoppingCart/buy', Buy_View.as_view(), name='Buy'),
    path('MyProducts', My_Products_View.as_view(), name='My Products'),
    path('MyProducts/add', Add_Products.as_view(), name='Add Products'),
    path('product/<int:pk>/edit', Edit_Product.as_view(), name='Edit Products'),
]
