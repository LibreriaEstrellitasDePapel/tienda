from .models import Cart, CartItem
def _ensure_session_key(request) -> str:
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key
def get_anonymous_cart(request, create=True):
    session_key = _ensure_session_key(request)
    qs = Cart.objects.filter(session_key=session_key, user__isnull=True, status=Cart.Status.OPEN)
    if qs.exists():
        return qs.first()
    if not create:
        return None
    return Cart.objects.create(session_key=session_key)
def get_user_cart(user, create=True):
    qs = Cart.objects.filter(user=user, status=Cart.Status.OPEN)
    if qs.exists():
        return qs.first()
    if not create:
        return None
    return Cart.objects.create(user=user)
def add_product(cart: Cart, product, qty=1):
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": qty})
    if not created:
        item.quantity += qty
        item.save()
    return item
def merge_carts(from_cart: Cart, to_cart: Cart):
    for item in from_cart.items.select_related("product"):
        add_product(to_cart, item.product, item.quantity)
    from_cart.status = Cart.Status.MERGED
    from_cart.save()