from django.contrib import admin
from .models import *
from .models import Size


# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ProductBrand)

admin.site.register(Size)
admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.register(Image)
admin.site.register(Review)
admin.site.register(ProductVariantPrice)
admin.site.register(ProductRating)
admin.site.register(Warehouse)
admin.site.register(Stock)
admin.site.register(Supplier)
admin.site.register(ColorVariants)

class variantImageAdmin(admin.StackedInline):
    model = variantImage

class ImageAdmin(admin.StackedInline):
    model = Image

class ProductVariantsAdmin(admin.ModelAdmin):    
    inlines = [variantImageAdmin]

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariants, ProductVariantsAdmin)


