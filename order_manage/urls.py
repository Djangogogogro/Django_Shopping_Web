from django.urls import path
from order_manage.views import (
    My_Order_View,
    Order_Manager
)

urlpatterns = [
    path("", My_Order_View.as_view(), name="My Order"),
    path("manager/", Order_Manager.as_view(), name="Order Manager"),
]
