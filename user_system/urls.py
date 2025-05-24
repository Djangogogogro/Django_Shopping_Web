# blog/urls.py
from django.urls import path
from .views import (
    Register_View,
    Customer_Login_View,
    logout_view,
    Add_To_Cart_View,
    Shopping_Cart_View
)

urlpatterns = [
    path("new/<str:model_type>", Register_View.as_view(), name="New User"),
    path("login/", Customer_Login_View.as_view(), name="Login"),
    path('logout/', logout_view, name='logout'),
    path('product/<int:pk>/add/', Add_To_Cart_View.as_view(), name='Add To Cart'),
    path('ShoppingCart', Shopping_Cart_View.as_view(), name='Shopping Cart'),
]
