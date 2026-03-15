from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .models import Order, OrderItem


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    size = request.POST.get('size', 'M')
    quantity = int(request.POST.get('quantity', 1))

    cart.add(product=product, size=size, quantity=quantity)

    if request.LANGUAGE_CODE == 'mn':
        messages.success(request, f'{product.name_mn} сагсанд нэмэгдлээ!')
    else:
        messages.success(request, f'{product.name} added to cart!')

    return redirect('orders:cart')


@require_POST
def cart_update(request, product_id, size):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    action = request.POST.get('action')

    if action == 'increase':
        cart.add(product=product, size=size, quantity=1)
    elif action == 'decrease':
        cart.add(product=product, size=size, quantity=-1)

    return redirect('orders:cart')


@require_POST
def cart_remove(request, product_id, size):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product, size)

    if request.LANGUAGE_CODE == 'mn':
        messages.success(request, 'Бүтээгдэхүүн сагснаас хасагдлаа.')
    else:
        messages.success(request, 'Item removed from cart.')

    return redirect('orders:cart')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})


def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        if request.LANGUAGE_CODE == 'mn':
            messages.warning(request, 'Таны сагс хоосон байна.')
        else:
            messages.warning(request, 'Your cart is empty.')
        return redirect('orders:cart')

    if request.method == 'POST':
        # Build customer name
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        customer_name = f"{first_name} {last_name}".strip()

        # Create order
        order = Order.objects.create(
            customer_name=customer_name,
            customer_email=request.POST.get('email'),
            customer_phone=request.POST.get('phone'),
            shipping_address=request.POST.get('address'),
            shipping_city=request.POST.get('city'),
            notes=request.POST.get('notes', ''),
            payment_method=request.POST.get('payment_method', 'qpay'),
        )

        # Create order items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                size=item['size'],
                price=item['price'],
                quantity=item['quantity'],
            )

        # Calculate and save totals
        order.calculate_totals()

        # Clear cart
        cart.clear()

        return redirect('orders:order_confirmation', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/confirmation.html', {'order': order})
