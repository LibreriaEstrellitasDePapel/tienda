from django.urls import path
from . import views
app_name = "catalog"
urlpatterns = [
    path("", views.store_home, name="home"),
    path("buscar/", views.search, name="search"),
    path("categoria/<slug:slug>/", views.category_view, name="category"),
    path("categoria/<slug:category_slug>/<slug:sub_slug>/", views.subcategory_view, name="subcategory"),
    path("producto/<slug:slug>/", views.product_detail, name="product"),
]
