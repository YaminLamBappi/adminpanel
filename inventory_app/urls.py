from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/edit/<int:pk>/', views.product_update, name='product_update'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/new/', views.create_order, name='create_order'),
    path('orders/<int:pk>/update/', views.order_update, name='order_update'),
    path('order-history/', views.order_history, name='order_history'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('supplier/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('categories/new/', views.create_category, name='create_category'),
    path('suppliers/new/', views.create_supplier, name='create_supplier'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
