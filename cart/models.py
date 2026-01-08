from django.conf import settings
from django.db import models
from django.db.models import F, Sum, DecimalField, ExpressionWrapper
class Cart(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CHECKED_OUT = "CHECKED_OUT", "Checked out"
        DISCARDED = "DISCARDED", "Discarded"
        MERGED = "MERGED", "Merged"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name="carts")
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)  # carrito anónimo
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def subtotal(self):
        # subtotal = sum(qty * price)
        return self.items.aggregate(
            s=Sum(
                ExpressionWrapper(F("quantity") * F("product__price"), output_field=DecimalField())
            )
        )["s"] or 0
    @property
    def total(self):
        # aquí puedes sumar envío/impuestos luego
        return self.subtotal
    def __str__(self):
        owner = self.user.username if self.user else self.session_key
        return f"Cart({owner})"
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["cart", "product"], name="uniq_product_per_cart")
        ]
    def __str__(self):
        return f"{self.product.title} x{self.quantity}"