from django.contrib.auth.views import LoginView
from django.urls import reverse
from .services import get_anonymous_cart, get_user_cart
class ShopLoginView(LoginView):
    template_name = "accounts/login.html"
    def get_success_url(self):
        # Ya autenticado
        anon = get_anonymous_cart(self.request, create=False)
        if anon and anon.items.exists():
            # Siempre damos la opción (ver ambos + decidir)
            return reverse("cart:resolve")
        return reverse("catalog:home")