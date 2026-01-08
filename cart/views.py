from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from catalog.models import Product
from .models import Cart
from .services import get_anonymous_cart, get_user_cart, add_product, merge_carts
def _active_cart_for_request(request):
    if request.user.is_authenticated:
        return get_user_cart(request.user)
    return get_anonymous_cart(request)
def cart_detail(request):
    anon = get_anonymous_cart(request, create=False)
    user_cart = get_user_cart(request.user, create=False) if request.user.is_authenticated else None
    active = _active_cart_for_request(request)
    return render(request, "cart/detail.html", {"cart": active, "anon_cart": anon, "user_cart": user_cart})
def cart_add(request, product_id):
    if request.method != "POST":
        return redirect("cart:detail")
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _active_cart_for_request(request)
    add_product(cart, product, qty=1)
    messages.success(request, "Producto añadido al carrito.")
    return redirect(product.get_absolute_url())
def cart_set_qty(request, item_id):
    if request.method != "POST":
        return redirect("cart:detail")
    cart = _active_cart_for_request(request)
    item = get_object_or_404(cart.items, id=item_id)
    qty = max(1, int(request.POST.get("qty", "1")))
    item.quantity = qty
    item.save()
    return redirect("cart:detail")
def cart_remove(request, item_id):
    cart = _active_cart_for_request(request)
    item = get_object_or_404(cart.items, id=item_id)
    item.delete()
    return redirect("cart:detail")
@login_required
def cart_resolve_after_login(request):
    """Pantalla post-login: ver ambos carritos y elegir:
    - usar carrito anónimo
    - mezclar
    - descartar carrito anónimo"""
    anon = get_anonymous_cart(request, create=False)
    user_cart = get_user_cart(request.user, create=True)
    if request.method == "POST":
        action = request.POST.get("action")
        if not anon or not anon.items.exists():
            return redirect("cart:detail")
        if action == "use_anon":
            # Descarta el carrito OPEN del usuario y adopta el anónimo
            if user_cart and user_cart.items.exists():
                user_cart.status = Cart.Status.DISCARDED
                user_cart.save()
            anon.user = request.user
            anon.session_key = None
            anon.save()
            messages.success(request, "Se usó el carrito anónimo como tu carrito principal.")
            return redirect("cart:detail")
        if action == "merge":
            merge_carts(anon, user_cart)
            messages.success(request, "Carritos mezclados.")
            return redirect("cart:detail")
        if action == "discard_anon":
            anon.status = Cart.Status.DISCARDED
            anon.save()
            messages.success(request, "Carrito anónimo descartado.")
            return redirect("cart:detail")
    return render(request, "cart/resolve.html", {"anon_cart": anon, "user_cart": user_cart})