from django.contrib import admin
from carparts.models import Product, ProductImage, Logo, Bodykit, SubscribeModel


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 6


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('producer', 'name', 'description', 'part_number', 'price', 'quantity', 'slug')
    inlines = [ProductImageInline]
    list_filter = ['producer']
    list_per_page = 25


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('logo_image',)


@admin.register((Bodykit))
class BodykitAdmin(admin.ModelAdmin):
    list_display = ('for_producer', 'image')


@admin.register(SubscribeModel)
class SubscribeModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_date', 'updated_date')