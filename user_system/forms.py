from django import forms
from showitem.models import Product, ProductImage

class CustomerLoginForm(forms.Form):
    user_mail = forms.EmailField(label="Email")
    user_password = forms.CharField(label="Password", widget=forms.PasswordInput)

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['category', 'name', 'price', 'description', 'quantity']

class ProductFormWithImages(forms.ModelForm):
    images = forms.FileField(
        widget=forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), 
        label="產品圖片",
        required=False
    )

    class Meta:
        model = Product  # 改為 Product 而不是 ProductImage
        fields = ['category', 'name', 'price', 'description', 'quantity']