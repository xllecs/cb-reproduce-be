from django.contrib import admin
from .models import Product, ProductImage, ProductSize, CartItem

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductSize)
admin.site.register(CartItem)
