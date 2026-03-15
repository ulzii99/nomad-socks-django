from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    name_mn = models.CharField(max_length=100, verbose_name="Нэр (Монгол)")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_name_display(self, language='mn'):
        return self.name_mn if language == 'mn' else self.name


class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small (US 5-7)'),
        ('M', 'Medium (US 8-10)'),
        ('L', 'Large (US 11-13)'),
    ]

    name = models.CharField(max_length=200)
    name_mn = models.CharField(max_length=200, verbose_name="Нэр (Монгол)")
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    description = models.TextField()
    description_mn = models.TextField(verbose_name="Тайлбар (Монгол)")

    price = models.DecimalField(max_digits=10, decimal_places=0, help_text="Үнэ (₮)")

    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # Product details
    material = models.CharField(max_length=200, default="80% хөвөн, 17% полиэстер, 3% эластан")

    # Stock management
    stock = models.PositiveIntegerField(default=0)

    # Flags
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def get_name_display(self, language='mn'):
        return self.name_mn if language == 'mn' else self.name

    def get_description_display(self, language='mn'):
        return self.description_mn if language == 'mn' else self.description

    @property
    def is_in_stock(self):
        return self.stock > 0

    def get_price_display(self):
        return f"₮{self.price:,.0f}"


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    feature = models.CharField(max_length=200)
    feature_mn = models.CharField(max_length=200, verbose_name="Онцлог (Монгол)")

    def __str__(self):
        return f"{self.product.name} - {self.feature}"

    def get_feature_display(self, language='mn'):
        return self.feature_mn if language == 'mn' else self.feature
