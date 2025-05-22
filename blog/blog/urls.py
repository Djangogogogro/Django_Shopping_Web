# blog/urls.py
from django.urls import path
from .views import (
    HomeView,
    Product_View,
    Register_View,
    Customer_Login_View,
    logout_view,
    Add_To_Cart_View,
    Shopping_Cart_View
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("product/<int:pk>/", Product_View.as_view(), name="Product Detail"),
    path("user/new/<str:model_type>", Register_View.as_view(), name="New User"),
    path("user/login/", Customer_Login_View.as_view(), name="Login"),
    path('logout/', logout_view, name='logout'),
    path('product/<int:pk>/add/', Add_To_Cart_View.as_view(), name='Add To Cart'),
    path('ShoppingCart', Shopping_Cart_View.as_view(), name='Shopping Cart'),
]
