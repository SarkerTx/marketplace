from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Cart is empty.')
        return redirect('product_list')
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price()
        )
        for item in cart:
            product = item['product']
            OrderItem.objects.create(
                order=order,
                product=product,
                vendor=product.vendor,
                price=item['price'],
                quantity=item['quantity'],
                total=item['total_price']
            )
            product.stock -= item['quantity']
            product.save()
        cart.clear()
        messages.success(request, 'Order placed successfully.')
        return redirect('order_detail', order_id=order.id)
    return render(request, 'orders/order_confirm.html', {'cart': cart})

@login_required
def order_detail(request, order_id):
    order = Order.objects.prefetch_related('items__product').get(id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order_list.html', {'orders': orders})