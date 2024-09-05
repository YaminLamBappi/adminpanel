from django import forms
from .models import Product, Category, Supplier, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'status', 'customer']  # Include 'customer'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.user = user
        product = kwargs.pop('product', None)
        if product:
            self.fields['product'].initial = product



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_info']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'supplier', 'price', 'stock_quantity', 'image']
        
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_info']
