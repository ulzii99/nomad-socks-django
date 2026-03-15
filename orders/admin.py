from django.contrib import admin
from .models import Order, OrderItem, ContactMessage


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'size', 'price', 'quantity', 'total_display']

    def total_display(self, obj):
        return obj.get_total_display()
    total_display.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'customer_phone', 'shipping_city',
                    'status', 'payment_method', 'get_total_display', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at', 'shipping_city']
    search_fields = ['customer_name', 'customer_email', 'customer_phone', 'shipping_address']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]

    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Shipping', {
            'fields': ('shipping_address', 'shipping_city')
        }),
        ('Order Details', {
            'fields': ('status', 'payment_method', 'notes')
        }),
        ('Totals', {
            'fields': ('subtotal', 'shipping_cost', 'total'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'subject', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
