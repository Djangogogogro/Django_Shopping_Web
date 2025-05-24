# blog/views.py
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect, get_object_or_404
from blog.forms import CustomerLoginForm
from django.urls import reverse_lazy
from blog.models import (
    Customer,
    Seller,
    Shopping_Cart,
    Order,
    Product
)

class HomeView(ListView):
    model = Product
    template_name = "home.html"

class Product_View(DetailView):
    model = Product
    template_name = "post_detail.html" 

class Register_View(CreateView):
    template_name = "post_new.html"
    fields = ["user_name", "user_mail", "user_password"]
    success_url = reverse_lazy('home')

    def get_model_class(self):
        model_type = self.kwargs.get('model_type')
        if model_type == 'customer':
            return Customer
        elif model_type == 'seller':
            return Seller
        else:
            raise ValueError("Invalid model type")
        
    def dispatch(self, request, *args, **kwargs):
        self.model = self.get_model_class()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        model = self.get_model_class()
        count = model.objects.count() + 1
        form.instance.user_ID = count

        form.instance.user_password = make_password(form.instance.user_password)

        return super().form_valid(form)
    
class Customer_Login_View(FormView):
    template_name = 'customer_login.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email = form.cleaned_data['user_mail']
        password = form.cleaned_data['user_password']

        try:
            customer = Customer.objects.get(user_mail=email)
            if check_password(password, customer.user_password):
                self.request.session['user_ID'] = customer.user_ID
                self.request.session['user_name'] = customer.user_name

                return super().form_valid(form)
            else:
                form.add_error(None, "password error")
                return self.form_invalid(form)
        except Customer.DoesNotExist:
            form.add_error('user_mail', "帳號不存在")
            return self.form_invalid(form)

def logout_view(request):
    request.session.flush()
    return redirect('home')

class Shopping_Cart_View(ListView):
    model = Shopping_Cart
    template_name = "shopping_cart.html"

class Add_To_Cart_View(View):
    def post(self, request, pk):
        customer_id = request.session.get('user_ID')
        if not customer_id:
            return redirect('Login')

        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get('quantity', 1))
        customer = get_object_or_404(Customer, user_ID=customer_id)

        cart_item, created = Shopping_Cart.objects.get_or_create(
            user_ID=customer,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('home')

