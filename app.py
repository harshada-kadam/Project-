from flask import Flask, request, redirect, url_for, render_template_string

# ----------------------------
# OOP CLASSES
# ----------------------------

class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class Cart:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.append(product)

    def total_price(self):
        return sum(product.price for product in self.items)

    def list_items(self):
        return self.items

class User:
    def __init__(self, username):
        self.username = username
        self.cart = Cart()

# ----------------------------
# FLASK APP SETUP
# ----------------------------

app = Flask(__name__)

# Sample product data
products = [
    Product(1, "Laptop", 60000),
    Product(2, "Smartphone", 30000),
    Product(3, "Headphones", 2500),
    Product(4, "Keyboard", 1200)
]

# Single user for simplicity
current_user = User("Harshada")

# ----------------------------
# HTML TEMPLATES AS STRINGS
# ----------------------------

index_html = """
<!DOCTYPE html>
<html>
<head><title>Shop</title></head>
<body>
    <h1>Products</h1>
    <ul>
        {% for product in products %}
            <li>
                {{ product.name }} - ₹{{ product.price }}
                <a href="{{ url_for('add_to_cart', product_id=product.id) }}">Add to Cart</a>
            </li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('cart') }}">Go to Cart</a>
</body>
</html>
"""

cart_html = """
<!DOCTYPE html>
<html>
<head><title>Cart</title></head>
<body>
    <h1>Your Cart</h1>
    {% if items %}
        <ul>
            {% for item in items %}
                <li>{{ item.name }} - ₹{{ item.price }}</li>
            {% endfor %}
        </ul>
        <p><strong>Total:</strong> ₹{{ total }}</p>
    {% else %}
        <p>Your cart is empty.</p>
    {% endif %}
    <a href="{{ url_for('index') }}">Continue Shopping</a>
</body>
</html>
"""

# ----------------------------
# ROUTES
# ----------------------------

@app.route('/')
def index():
    return render_template_string(index_html, products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if product:
        current_user.cart.add_product(product)
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = current_user.cart.list_items()
    total = current_user.cart.total_price()
    return render_template_string(cart_html, items=cart_items, total=total)

# ----------------------------
# RUN SERVER
# ----------------------------

if __name__ == '__main__':
    app.run(debug=True)
