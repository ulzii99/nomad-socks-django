from django.db import migrations


def add_product(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Product = apps.get_model('products', 'Product')
    ProductFeature = apps.get_model('products', 'ProductFeature')

    # Get or create category
    cat, _ = Category.objects.get_or_create(
        slug='casual',
        defaults={'name': 'Casual', 'name_mn': 'Энгийн'}
    )

    # Check if product exists
    if not Product.objects.filter(slug='classic-black-socks').exists():
        product = Product.objects.create(
            name='Classic Black Socks',
            name_mn='Хар сонгодог оймс',
            slug='classic-black-socks',
            category=cat,
            description='Timeless black socks for any occasion. Perfect for work or casual wear.',
            description_mn='Ямар ч үед тохиромжтой сонгодог хар оймс. Ажил эсвэл өдөр тутмын хувцасанд тохиромжтой.',
            price=12000,
            material='80% Cotton, 18% Polyester, 2% Elastane',
            image_url='https://m.media-amazon.com/images/I/71uBkXKTRIL._AC_UY1000_.jpg',
            is_active=True,
            is_featured=True,
        )
        ProductFeature.objects.create(product=product, feature='Soft cotton blend', feature_mn='Зөөлөн хөвөн холимог')
        ProductFeature.objects.create(product=product, feature='Anti-odor technology', feature_mn='Үнэр эсэргүүцэх технологи')


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_image_url'),
    ]

    operations = [
        migrations.RunPython(add_product, reverse_func),
    ]
