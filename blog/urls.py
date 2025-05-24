# blog/urls.py
from django.urls import path
from .views import (
    HomeView,
    Product_View,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("product/<int:pk>/", Product_View.as_view(), name="Product Detail"),
]
