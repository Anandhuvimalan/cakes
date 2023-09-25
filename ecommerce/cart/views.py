from django.shortcuts import render, redirect, get_object_or_404
import uuid
from django.core.exceptions import ObjectDoesNotExist
from shop.models import Product
from .models import Cart, CartItem
from django.http import JsonResponse

def _cart_id(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart_id = str(uuid.uuid4())
        request.session['cart_id'] = cart_id
    return cart_id


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    requested_quantity = int(request.GET.get('quantity', 1))
    cart_id = _cart_id(request)

    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id)
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        max_quantity = product.stock - cart_item.quantity
        
        if requested_quantity <= max_quantity:
            new_quantity = cart_item.quantity + requested_quantity
            
            if new_quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
        else:
            return render(request, 'cart_stock_alert.html', {'product_name': product.name, 'max_quantity': max_quantity})
    except CartItem.DoesNotExist:
        if requested_quantity <= product.stock:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=requested_quantity,
                cart=cart
            )
            cart_item.save()
        else:
            return render(request, 'cart_stock_alert.html', {'product_name': product.name, 'max_quantity': product.stock})

    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))


def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    if cart_item.cart.cart_id == _cart_id(request):
        cart_item.delete()
    
    return redirect('cart:cart_detail')