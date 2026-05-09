from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import VendorProfile
from products.models import Product
from .forms import ProductForm
from orders.models import OrderItem

@login_required
def vendor_dashboard(request):
    # Only vendors can enter
    if not request.user.is_vendor():
        messages.error(request, 'Access denied.')
        return redirect('home')
    vendor = request.user.vendor_profile
    if not vendor.is_approved:
        messages.warning(request, 'Your vendor account is pending approval.')
    products = Product.objects.filter(vendor=vendor)
    return render(request, 'vendors/dashboard.html', {'vendor': vendor, 'products': products})

@login_required
def add_product(request):
    if not request.user.is_vendor() or not request.user.vendor_profile.is_approved:
        messages.error(request, 'Not allowed.')
        return redirect('home')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor_profile
            product.save()
            messages.success(request, 'Product added.')
            return redirect('vendor_dashboard')
    else:
        form = ProductForm()
    return render(request, 'vendors/product_form.html', {'form': form})

@login_required
def edit_product(request, pk):
    vendor = request.user.vendor_profile
    product = get_object_or_404(Product, pk=pk, vendor=vendor)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated.')
            return redirect('vendor_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'vendors/product_form.html', {'form': form})

@login_required
def delete_product(request, pk):
    vendor = request.user.vendor_profile
    product = get_object_or_404(Product, pk=pk, vendor=vendor)
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect('vendor_dashboard')

@login_required
def vendor_orders(request):
    vendor = request.user.vendor_profile
    order_items = OrderItem.objects.filter(vendor=vendor).select_related('order', 'product').order_by('-order__created')
    return render(request, 'vendors/orders.html', {'order_items': order_items})