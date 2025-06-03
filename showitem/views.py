from django.shortcuts import render, get_object_or_404
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

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

def semantic_search(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        # 載入向量模型
        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_vector = model.encode([query])

        # 載入 FAISS index 和 ID 對應
        index = faiss.read_index("vector_store/product_index.faiss")
        product_ids = np.load("vector_store/product_ids.npy")

        # 查詢最近的 10 筆
        distances, indices = index.search(query_vector, k=10)

        # 找出對應的 Product ID
        matched_ids = product_ids[indices[0]]
        results = Product.objects.filter(id__in=matched_ids)

    return render(request, "semantic_search.html", {
        "query": query,
        "results": results
    })


def product_list(request):
    query = request.GET.get('q', '')
    categories = Category.objects.all()

    use_semantic = True
    all_products = Product.objects.none()

    if query:
        if use_semantic:
            try:
                model = SentenceTransformer("all-MiniLM-L6-v2")
                query_vector = model.encode([query])
                index = faiss.read_index("vector_store/product_index.faiss")
                product_ids = np.load("vector_store/product_ids.npy")

                distances, indices = index.search(query_vector, k=12)
                matched_ids = product_ids[indices[0]]

                from django.db.models import Case, When
                preserved_order = Case(*[
                    When(id=int(pk), then=pos) for pos, pk in enumerate(matched_ids)
                ])
                all_products = Product.objects.filter(id__in=matched_ids).order_by(preserved_order)
            except Exception as e:
                print(f"Semantic search error: {e}")
                all_products = Product.objects.filter(name__icontains=query)
        else:
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
        'products_by_category': products_by_category,
        'query': query,
    })

