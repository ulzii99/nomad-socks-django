from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact', {
            'fields': ('email', 'phone')
        }),
        ('Address', {
            'fields': ('address', 'address_mn')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url')
        }),
        ('Branding', {
            'fields': ('tagline', 'tagline_mn')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
