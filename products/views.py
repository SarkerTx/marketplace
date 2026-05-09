from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.filter(available=True, vendor__is_approved=True).select_related('vendor')
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('vendor'), pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})