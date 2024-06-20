class Cart():
    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def get_cart_books_count(self):
        return sum(libro['cantidad'] for libro in self.cart.values())

    def get_total_price(self):
        return sum(libro['precio'] * libro['cantidad'] for libro in self.cart.values())

    def save_cart(self):
        self.session['cart'] = self.cart
        self.session['cart_books_count'] = self.get_cart_books_count()
        self.session.modified = True

    def add_to_cart(self, libro):
        libro_id = str(libro.id)

        if libro_id not in self.cart:
            self.cart[libro_id] = {
                'id': libro.id,
                'isbn': libro.isbn,
                'portada': libro.portada.url if libro.portada else None,
                'titulo': libro.titulo,
                'autor': libro.autor,
                'precio': float(libro.precio),
                'stock': libro.stock,
                'cantidad': 1,
                'total': float(libro.precio),
            }
        else:
            self.cart[libro_id]['cantidad'] += 1

            self.cart[libro_id]['total'] += float(libro.precio)

        self.save_cart()

    def remove_from_cart(self, libro_id):
        libro_id = str(libro_id)

        if libro_id in self.cart:
            if self.cart[libro_id]['cantidad'] > 1:
                self.cart[libro_id]['cantidad'] -= 1
                self.cart[libro_id]['total'] -= self.cart[libro_id]['precio']
            else:
                del self.cart[libro_id]

            self.save_cart()

    def clear_cart(self):
        self.session['cart'] = {}
        self.session['cart_books_count'] = 0
        self.session.modified = True
