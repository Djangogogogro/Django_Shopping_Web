from django.contrib import admin

# Register your models here.
from .models import Category, Product, ProductImage

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class ProductImageInline(admin.TabularInline):  # 或 StackedInline
    model = ProductImage
    extra = 1  # 預設多一欄空白可以新增

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'quantity')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]  # 讓你在 Product 頁面內直接新增圖片

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image_path')

# 註冊自訂的 Admin 類別
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
