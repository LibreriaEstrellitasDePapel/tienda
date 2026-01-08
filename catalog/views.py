from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Category, SubCategory, Product
def store_home(request):
    categories = Category.objects.all().order_by("name")
    products = Product.objects.filter(is_active=True).order_by("title")
    return render(request, "catalog/home.html", {"categories": categories, "products": products})
def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = category.subcategories.all().order_by("name")
    products = category.products.filter(is_active=True).order_by("title")
    return render(request, "catalog/category.html", {"category": category, "subcategories": subcategories, "products": products})
def subcategory_view(request, category_slug, sub_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcat = get_object_or_404(SubCategory, category=category, slug=sub_slug)
    products = subcat.products.filter(is_active=True).order_by("title")
    return render(request, "catalog/subcategory.html", {"category": category, "subcategory": subcat, "products": products})
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "catalog/product_detail.html", {"product": product})
def search(request):
    q = (request.GET.get("q") or "").strip()
    categories = subcategories = products = []
    if q:
        categories = Category.objects.filter(name__icontains=q)
        subcategories = SubCategory.objects.filter(name__icontains=q).select_related("category")
        products = Product.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(authors_or_brands__icontains=q),
            is_active=True)
    return render(request, "catalog/search.html", {"q": q, "categories": categories, "subcategories": subcategories, "products": products})