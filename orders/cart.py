from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    """Session-based shopping cart"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, size='M', quantity=1, update_quantity=False):
        """Add product to cart or update quantity"""
        product_id = str(product.id)
        key = f"{product_id}_{size}"

        if key not in self.cart:
            self.cart[key] = {
                'product_id': product_id,
                'size': size,
                'quantity': 0,
                'price': str(product.price),
            }

        if update_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity

        self.save()

    def remove(self, product_id, size):
        """Remove item from cart"""
        key = f"{product_id}_{size}"
        if key in self.cart:
            del self.cart[key]
            self.save()

    def save(self):
        """Mark session as modified"""
        self.session.modified = True

    def __iter__(self):
        """Iterate over cart items and fetch products from DB"""
        product_ids = set()
        for key, item in self.cart.items():
            product_ids.add(item['product_id'])

        products = Product.objects.filter(id__in=product_ids)
        products_dict = {str(p.id): p for p in products}

        cart_copy = self.cart.copy()
        for key, item in cart_copy.items():
            product = products_dict.get(item['product_id'])
            if product:
                item['product'] = product
                item['total_price'] = Decimal(item['price']) * item['quantity']
                yield item

    def __len__(self):
        """Count total items in cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate total price"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_total_display(self):
        """Format total with currency"""
        return f"₮{self.get_total_price():,.0f}"

    def clear(self):
        """Clear the cart"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_items_count(self):
        """Get number of unique items"""
        return len(self.cart)
