from .cart import Cart

def counter(request):
    cart = Cart(request)
    return dict(item_count=cart.__len__())
