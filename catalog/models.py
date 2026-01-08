from django.db import models
from django.urls import reverse
from django.utils.text import slugify
class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("catalog:category", args=[self.slug])
    def __str__(self):
        return self.name
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["category", "slug"], name="uniq_subcat_slug_per_category")
        ]
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("catalog:subcategory", args=[self.category.slug, self.slug])
    def __str__(self):
        return f"{self.category.name} / {self.name}"
class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    subcategories = models.ManyToManyField(SubCategory, blank=True, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    authors_or_brands = models.CharField(max_length=255, blank=True)  # opcional
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("catalog:product", args=[self.slug])
    def __str__(self):
        return self.title