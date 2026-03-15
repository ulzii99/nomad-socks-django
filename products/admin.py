from django.contrib import admin
from .models import Category, Product, ProductFeature


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_mn', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'name_mn']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_mn', 'category', 'price', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active', 'is_featured', 'category', 'created_at']
    list_editable = ['is_active', 'is_featured', 'price']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'name_mn', 'description', 'description_mn']
    inlines = [ProductFeatureInline]
    fieldsets = (
        ('English', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Монгол', {
            'fields': ('name_mn', 'description_mn')
        }),
        ('Details', {
            'fields': ('category', 'price', 'material', 'image')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
    )
