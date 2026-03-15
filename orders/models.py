from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Хүлээгдэж буй'),
        ('confirmed', 'Баталгаажсан'),
        ('paid', 'Төлбөр хийгдсэн'),
        ('shipped', 'Илгээгдсэн'),
        ('delivered', 'Хүргэгдсэн'),
        ('cancelled', 'Цуцлагдсан'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('qpay', 'QPay'),
        ('socialpay', 'SocialPay'),
        ('bank_transfer', 'Банкны шилжүүлэг'),
        ('cash', 'Бэлэн мөнгө'),
    ]

    # Customer info
    customer_name = models.CharField(max_length=200, verbose_name="Нэр")
    customer_email = models.EmailField(verbose_name="Имэйл")
    customer_phone = models.CharField(max_length=20, verbose_name="Утасны дугаар")

    # Shipping address
    shipping_address = models.TextField(verbose_name="Хүргэлтийн хаяг")
    shipping_city = models.CharField(max_length=100, default="Улаанбаатар", verbose_name="Хот")

    # Order details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    payment_id = models.CharField(max_length=100, blank=True, help_text="QPay/SocialPay transaction ID")

    # Totals
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    # Notes
    notes = models.TextField(blank=True, verbose_name="Тэмдэглэл")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Захиалга #{self.id} - {self.customer_name}"

    def get_total_display(self):
        return f"₮{self.total:,.0f}"

    def calculate_totals(self):
        self.subtotal = sum(item.get_total() for item in self.items.all())
        self.total = self.subtotal + self.shipping_cost
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=5)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)  # Price at time of order

    def __str__(self):
        return f"{self.quantity}x {self.product.name} ({self.size})"

    def get_total(self):
        return self.price * self.quantity

    def get_total_display(self):
        return f"₮{self.get_total():,.0f}"


class ContactMessage(models.Model):
    """Store contact form submissions"""
    SUBJECT_CHOICES = [
        ('general', 'Ерөнхий асуулт'),
        ('order', 'Захиалга өгөх'),
        ('shipping', 'Хүргэлтийн асуулт'),
        ('wholesale', 'Бөөний худалдааны асуулт'),
        ('other', 'Бусад'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
