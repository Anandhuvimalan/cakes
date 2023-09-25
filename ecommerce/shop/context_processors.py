# shop context_processors.py

from .models import Category
from cart.models import CartItem  # Import the CartItem model

def menu_links(request):
    links = Category.objects.all()
    
    # Calculate the cart item count
    cart_item_count = 0
    if 'cart_id' in request.session:
        cart_id = request.session['cart_id']
        cart_item_count = CartItem.objects.filter(cart__cart_id=cart_id, active=True).count()
    
    return {'links': links, 'cart_item_count': cart_item_count}
