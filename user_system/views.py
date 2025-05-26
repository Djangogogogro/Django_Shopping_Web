# blog/views.py
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect, get_object_or_404
from user_system.forms import CustomerLoginForm
from django.contrib import messages
from django.urls import reverse_lazy
from user_system.models import (
    Customer,
    Seller,
    Shopping_Cart,
    Order,
    Product
)

class Register_View(CreateView):
    template_name = "post_new.html"
    fields = ["user_name", "user_mail", "user_password"]
    success_url = reverse_lazy('home')

    def get_model_class(self):
        self.model_type = self.kwargs.get('model_type')
        if self.model_type == 'customer':
            return Customer
        elif self.model_type == 'seller':
            return Seller
        else:
            raise ValueError("Invalid model type")
        
    def dispatch(self, request, *args, **kwargs):
        self.model = self.get_model_class()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_type'] = self.kwargs.get('model_type')
        return context

    def form_valid(self, form):
        model = self.get_model_class()
        count = model.objects.count() + 1
        form.instance.user_ID = f'{(self.model_type[0]).upper()}{str(count)}'

        form.instance.user_password = make_password(form.instance.user_password)

        return super().form_valid(form)
    
class Login_View(FormView):
    template_name = 'login.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy('home')

    def get_model_class(self):
        self.model_type = self.kwargs.get('model_type')
        if self.model_type == 'customer':
            return Customer
        elif self.model_type == 'seller':
            return Seller
        else:
            raise ValueError("Invalid model type")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_type'] = self.kwargs.get('model_type')
        return context

    def form_valid(self, form):
        email = form.cleaned_data['user_mail']
        password = form.cleaned_data['user_password']
        model = self.get_model_class()

        try:
            customer = model.objects.get(user_mail=email)
            if check_password(password, customer.user_password):
                self.request.session['user_ID'] = customer.user_ID
                self.request.session['user_name'] = customer.user_name

                return super().form_valid(form)
            else:
                form.add_error(None, "password error")
                return self.form_invalid(form)
        except model.DoesNotExist:
            form.add_error('user_mail', "帳號不存在")
            return self.form_invalid(form)

def logout_view(request):
    request.session.flush()
    return redirect('home')

class Shopping_Cart_View(ListView):
    model = Shopping_Cart
    template_name = "shopping_cart.html"
    context_object_name = "cart_items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ID = self.request.session.get('user_ID')
        total = 0
        for item in context['cart_items']:
            if item.user_ID.user_ID == user_ID:
                total += item.product.price * item.quantity
        context['total'] = total
        return context

class Add_To_Cart_View(View):
    def post(self, request, pk):
        customer_id = request.session.get('user_ID')
        if not customer_id:
            return redirect('Login')

        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get('quantity', 1))
        customer = get_object_or_404(Customer, user_ID=customer_id)


        if quantity <= product.quantity:

            product.quantity -= quantity
            product.save()

            cart_item, created = Shopping_Cart.objects.get_or_create(
                user_ID=customer,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

        else:
            messages.error(self.request, "Not enough product")


        return redirect('Product Detail', pk=pk)

class My_Products_View(ListView):
    model = Product
    template_name = "my_products.html"
    context_object_name = "products"

    def get_queryset(self):
        user_id = self.request.session.get('user_ID')
        if not user_id:
            return redirect('Login')
        try:
            seller = Seller.objects.get(user_ID=user_id)
            return seller.products.all()
        except Seller.DoesNotExist:
            return Product.objects.none()

class Add_Products(CreateView):
    model = Product
    template_name = "add_products.html"
    fields = ["name", "price", "quantity"]
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        current_user_id = self.request.session.get('user_ID')
        if not current_user_id:
            return redirect('Login')

        response = super().form_valid(form)
        count = Product.objects.count()
        if form.cleaned_data['quantity'] != 0:
            is_product_state = 'IS' #in stock
        form.instance.product_ID = f'{is_product_state}_{str(count)}'
        self.object.save()

        seller = Seller.objects.get(user_ID = current_user_id)
        seller.products.add(self.object)

        return response
