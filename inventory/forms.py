
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'sku',
            'category',
            'quantity',
            'price',
            'reorder_level',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product name',
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unique product SKU',
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01',
            }),
            'reorder_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
        }
