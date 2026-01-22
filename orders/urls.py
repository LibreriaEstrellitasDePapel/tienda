from django.urls import path
from . import views
app_name="orders"
urlpatterns=[
    path("checkout/",views.checkout_cart,name="checkout_cart"),
    path("buy-now/<int:product_id>/",views.buy_now,name="buy_now")
]