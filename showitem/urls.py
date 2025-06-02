from django.urls import path
from .views import product_list, product_detail
from django.conf import  settings
from django.conf.urls.static import static
urlpatterns = [
    path('', product_list, name = 'product_list'),
    path('product/<int:product_id>/',product_detail, name = 'product_detail'),
]
