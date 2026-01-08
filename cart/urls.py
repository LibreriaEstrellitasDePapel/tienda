from django.urls import path
from . import views
app_name = "cart"
urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("add/<int:product_id>/", views.cart_add, name="add"),
    path("set-qty/<int:item_id>/", views.cart_set_qty, name="set_qty"),
    path("remove/<int:item_id>/", views.cart_remove, name="remove"),
    path("resolve/", views.cart_resolve_after_login, name="resolve"),
]
