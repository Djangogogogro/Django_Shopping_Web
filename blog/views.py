# blog/views.py
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from blog.models import (
    Product
)

class HomeView(ListView):
    model = Product
    template_name = "home.html"

class Product_View(DetailView):
    model = Product
    template_name = "post_detail.html" 