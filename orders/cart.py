CART_SESSION_KEY = 'cart'


class CartItem:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = request.session[CART_SESSION_KEY] = {}
        self.cart = cart
