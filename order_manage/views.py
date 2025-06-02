from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from collections import defaultdict
from datetime import timedelta
from django.utils import timezone

from user_system.models import (
    Order,
    Seller
)
from showitem.models import (
    Product
)

class My_Order_View(ListView):
    model = Order
    template_name = "my_order.html"
    context_object_name = "order_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ID = self.request.session.get('user_ID')

        display_orders = []

        for order in context['order_list']:
            if (user_ID == order.customer_ID.user_ID) or (user_ID == order.seller_ID.user_ID):
                all_product = order.products
                product_lines = []
                total = 0

                product_entries = all_product.split(',')[:-1]
                for entry in product_entries:
                    product_ID, price, quantity = entry.split('|')
                    product = get_object_or_404(Product, name=product_ID)
                    line = f"{product.name} x{quantity}"
                    product_lines.append(line)
                    total += int(price) * int(quantity)

                if 'C' in user_ID:
                    name_line = f"Seller: {order.seller_ID.user_name}"
                else:
                    name_line = f"Customer: {order.customer_ID.user_name}"

                display_orders.append({
                    "product_lines": product_lines,
                    "total": total,
                    "date": order.date,
                    "name_line": name_line
                })

        context['display_orders'] = display_orders
        return context
    
class Order_Manager(ListView):
    model = Order
    template_name = 'order_manager.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_ID = self.request.session.get('user_ID')
        selected_product_id = self.request.GET.get("name")

        # ========== 銷量統計 ==========
        product_sales = defaultdict(int)
        seller_orders = Order.objects.filter(seller_ID__user_ID=user_ID)

        for order in seller_orders:
            product_entries = order.products.split(',')[:-1]
            for entry in product_entries:
                product_ID, price, quantity = entry.split('|')
                product = get_object_or_404(Product, name=product_ID)
                product_sales[product.name] += int(quantity)

        context['product_labels'] = list(product_sales.keys())
        context['product_data'] = list(product_sales.values())

        # ========== 銷售額統計 ==========
        days = int(self.request.GET.get("days", 5))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days - 1)

        date_labels = [(start_date + timedelta(days=i)) for i in range(days)]
        daily_sales = {date: 0 for date in date_labels}

        seller_orders_in_range = seller_orders.filter(date__range=(start_date, end_date))
        for order in seller_orders_in_range:
            total = 0
            product_entries = order.products.split(',')[:-1]
            for entry in product_entries:
                _, price, quantity = entry.split('|')
                total += int(price) * int(quantity)
            if order.date in daily_sales:
                daily_sales[order.date] += total

        context["daily_labels"] = [d.strftime("%Y-%m-%d") for d in date_labels]
        context["daily_data"] = list(daily_sales.values())
        context["days"] = days

        # ========== 單一商品每日銷量 ==========
        product_choices = get_object_or_404(Seller, user_ID = user_ID).products.all()
        single_daily_sales = {date: 0 for date in date_labels}

        if selected_product_id:
            for order in seller_orders_in_range:
                total = 0
                product_entries = order.products.split(',')[:-1]
                for entry in product_entries:
                    name, price, quantity = entry.split('|')
                    if name == str(self.request.GET.get("name", 0)):
                        total += int(price) * int(quantity)
                if order.date in single_daily_sales:
                    single_daily_sales[order.date] += total

        context["single_product_labels"] = [d.strftime("%Y-%m-%d") for d in date_labels]
        context["single_product_data"] = list(single_daily_sales.values())
        context["product_choices"] = product_choices
        context["selected_product_id"] = selected_product_id or ""
        

        return context