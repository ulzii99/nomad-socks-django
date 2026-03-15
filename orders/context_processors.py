from .cart import Cart


def cart_context(request):
    """Add cart to template context globally"""
    return {'cart': Cart(request)}
