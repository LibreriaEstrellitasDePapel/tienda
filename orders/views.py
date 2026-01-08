from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from cart.services import get_user_cart
from .models import Order, OrderItem
from catalog.models import Product
from cart.models import Cart
@login_required
def checkout_cart(request):
    cart = get_user_cart(request.user, create=False)
    if not cart or not cart.items.exists():
        return redirect("cart:detail")
    if request.method == "POST":
        order = Order.objects.create(user=request.user, status=Order.Status.PLACED)
        for item in cart.items.select_related("product"):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price,)
        cart.status = Cart.Status.CHECKED_OUT
        cart.save()
        return render(request, "orders/success.html", {"order": order})
    return render(request, "orders/checkout_cart.html", {"cart": cart})
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip()
        order = Order.objects.create(email=email, status=Order.Status.PLACED)
        OrderItem.objects.create(order=order, product=product, quantity=1, unit_price=product.price)
        return render(request, "orders/success.html", {"order": order})
    return render(request, "orders/buy_now.html", {"product": product})