from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Supplier, Order
from .forms import ProductForm, CategoryForm, SupplierForm, OrderForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.dateparse import parse_date


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_create')  # Adjust if necessary
    else:
        form = CategoryForm()
    return render(request, 'inventory_app/category_form.html', {'form': form})

def create_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_create')  # Adjust if necessary
    else:
        form = SupplierForm()
    return render(request, 'inventory_app/supplier_form.html', {'form': form})

def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    context = {
        'supplier': supplier,
    }
    return render(request, 'inventory_app/supplier_detail.html', context)


def create_order(request):
    # Get product ID from query parameters
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.user = request.user
            order.save()
            return redirect('order_list')
    else:
        form = OrderForm(user=request.user)
        form.fields['product'].initial = product

    return render(request, 'inventory_app/order_form.html', {'form': form, 'product': product})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    product = order.product
    context = {
        'order': order,
        'product': product,
    }
    return render(request, 'inventory_app/order_detail.html', context)

def order_list(request):
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    orders = Order.objects.all()

    if search_query:
        if search_query.isdigit():
            orders = orders.filter(id=search_query)
        else:
            orders = orders.filter(
                Q(product__name__icontains=search_query) |
                Q(user__username__icontains=search_query) 
            )

    if start_date:
        orders = orders.filter(order_date__gte=start_date)

    if end_date:
        orders = orders.filter(order_date__lte=end_date)

    orders = orders.order_by('order_date')  # Sort by order_date in ascending order

    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'inventory_app/order_list.html', context)

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'inventory_app/order_update.html', {'form': form, 'order': order})


def order_history(request):
    orders = Order.objects.filter(user=request.user, status='delivered').order_by('-order_date')
    
    search_query = request.GET.get('search', '')
    if search_query:
        if search_query.isdigit():
            orders = orders.filter(id=search_query)
        else:
            orders = orders.filter(
                Q(product__name__icontains=search_query) |
                Q(user__username__icontains=search_query) 
            )
    # Handle date filtering
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    
    if start_date_str:
        start_date = parse_date(start_date_str)
        orders = orders.filter(order_date__gte=start_date)
        
    if end_date_str:
        end_date = parse_date(end_date_str)
        orders = orders.filter(order_date__lte=end_date)
    
    # Sort orders by date
    orders = orders.order_by('-order_date')
    
    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        

    return render(request, 'inventory_app/order_history.html', {
        'orders': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'start_date': start_date_str,
        'end_date': end_date_str,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'inventory_app/product_detail.html', context)


def product_list(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    products = Product.objects.all()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(id__iexact=search_query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    # Pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'inventory_app/product_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'categories': categories,
    })


def product_create(request, pk=None):
    if pk:
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    else:
        form = ProductForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        form.save()
        return redirect('product_list')  # Adjust redirect target as needed

    return render(request, 'inventory_app/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory_app/product_form.html', {'form': form})


