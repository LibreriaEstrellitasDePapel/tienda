from .services import get_anonymous_cart, get_user_cart
def cart_badge(request):
    cart = get_user_cart(request.user, create=False) if request.user.is_authenticated else get_anonymous_cart(request, create=False)
    count = 0
    if cart:
        count = sum(i.quantity for i in cart.items.all())
    return {"cart_count": count}