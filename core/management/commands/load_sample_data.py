from django.core.management.base import BaseCommand
from products.models import Category, Product, ProductFeature


class Command(BaseCommand):
    help = 'Load sample products'

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write('Products already exist')
            return

        # Create categories
        cat_traditional, _ = Category.objects.get_or_create(
            slug='traditional',
            defaults={'name': 'Traditional', 'name_mn': 'Уламжлалт'}
        )
        cat_casual, _ = Category.objects.get_or_create(
            slug='casual',
            defaults={'name': 'Casual', 'name_mn': 'Энгийн'}
        )

        products_data = [
            {
                'name': 'Mongolian Pattern Socks',
                'name_mn': 'Монгол хээтэй оймс',
                'slug': 'mongolian-pattern',
                'description': 'Traditional Mongolian patterns on comfortable everyday socks.',
                'description_mn': 'Өдөр тутмын тухтай оймс дээр уламжлалт Монгол хээ.',
                'price': 15000,
                'material': 'Cotton blend',
                'category': cat_traditional,
                'is_featured': True,
            },
            {
                'name': 'Nomad Rider Socks',
                'name_mn': 'Нүүдэлчин морьтон оймс',
                'slug': 'nomad-rider',
                'description': 'Durable socks inspired by the Mongolian nomadic lifestyle.',
                'description_mn': 'Монголын нүүдэлчин амьдралаас санаа авсан бат бөх оймс.',
                'price': 18000,
                'material': 'Wool blend',
                'category': cat_traditional,
                'is_featured': True,
            },
            {
                'name': 'Everyday Comfort Socks',
                'name_mn': 'Өдөр тутмын тохитой оймс',
                'slug': 'everyday-comfort',
                'description': 'Soft and comfortable socks for daily wear.',
                'description_mn': 'Өдөр бүр өмсөхөд зөөлөн, тухтай оймс.',
                'price': 12000,
                'material': '100% Cotton',
                'category': cat_casual,
                'is_featured': True,
            },
            {
                'name': 'Steppe Blue Socks',
                'name_mn': 'Тал нутгийн цэнхэр оймс',
                'slug': 'steppe-blue',
                'description': 'Sky blue socks inspired by the Mongolian steppe.',
                'description_mn': 'Монголын тал нутгийн тэнгэр цэнхэр өнгөтэй оймс.',
                'price': 14000,
                'material': 'Cotton blend',
                'category': cat_casual,
                'is_featured': True,
            },
        ]

        for p in products_data:
            product = Product.objects.create(**p)
            ProductFeature.objects.create(
                product=product,
                feature='Breathable fabric',
                feature_mn='Агаар нэвтрүүлдэг даавуу'
            )
            ProductFeature.objects.create(
                product=product,
                feature='Reinforced heel and toe',
                feature_mn='Бэхжүүлсэн өсгий ба хуруу'
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(products_data)} products'))
