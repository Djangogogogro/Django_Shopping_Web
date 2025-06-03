from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Category, Product

# def product_list(request):
#     category_id = request.GET.get('category')  # 從 URL 取得 category 參數
#     categories = Category.objects.all()

#     if category_id:
#         products = Product.objects.filter(category_id=category_id).prefetch_related('images')
#     else:
#         products = Product.objects.all().prefetch_related('images')

#     return render(request, 'product_list.html', {
#         'products': products,
#         'categories': categories,
#         'selected_category': int(category_id) if category_id else None,
#     })


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk = product_id)
    user_id = request.session.get('user_ID')
    return render(request, 'product_detail.html',{'product':product, 'userID':user_id})




def product_list(request):
    query = request.GET.get('q', '')
    categories = Category.objects.all()
    
    if query:
        all_products = Product.objects.filter(name__icontains=query)
    else:
        all_products = Product.objects.all()

    products_by_category = {
        category.id: Product.objects.filter(category=category)
        for category in categories
    }

    return render(request, 'product_list.html', {
        'categories': categories,
        'all_products': all_products,
        'products_by_category': products_by_category
    })

