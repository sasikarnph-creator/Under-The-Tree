import os
from flask import Flask, render_template, session, jsonify, request, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-key')

PRODUCTS = [
    {"id": 1, "name": "The Silent Garden", "category": "โรแมนติก", "price": 12.99, "image": "static/images/product1.svg", "desc": "นิยายโรแมนติกอบอุ่นหัวใจ สำหรับคนรักความทรงจำ"},
    {"id": 2, "name": "Moonlit Voyage", "category": "แฟนตาซี", "price": 14.50, "image": "static/images/product2.svg", "desc": "การผจญภัยในโลกเวทมนตร์ที่เต็มไปด้วยปริศนา"},
    {"id": 3, "name": "Whispers in the Alley", "category": "นิยายสืบสวน", "price": 11.00, "image": "static/images/product3.svg", "desc": "นิยายสืบสวนที่ชวนให้คุณติดตามจนจบ"},
    {"id": 4, "name": "The Forgotten Library", "category": "แฟนตาซี", "price": 16.75, "image": "static/images/product4.svg", "desc": "เรื่องราวแห่งห้องสมุดลี้ลับและการค้นพบ"},
    {"id": 5, "name": "Letters to Yesterday", "category": "โรแมนติก", "price": 9.99, "image": "static/images/product5.svg", "desc": "จดหมายจากอดีตที่เปลี่ยนชีวิตใครบางคน"},
    {"id": 6, "name": "The Night Detective", "category": "นิยายสืบสวน", "price": 13.25, "image": "static/images/product6.svg", "desc": "นักสืบผู้ไขคดีในยามค่ำคืนกับเงื่อนงำลึกลับ"},
]


def find_product(pid):
    return next((p for p in PRODUCTS if p["id"] == int(pid)), None)


def get_cart():
    return session.setdefault('cart', {})


def cart_count():
    cart = get_cart()
    return sum(cart.values())


def cart_details():
    cart = get_cart()
    items = []
    total = 0.0
    for pid_s, qty in cart.items():
        pid = int(pid_s)
        p = find_product(pid)
        if not p:
            continue
        subtotal = p['price'] * qty
        total += subtotal
        items.append({
            'product': p,
            'qty': qty,
            'subtotal': subtotal
        })
    return items, total


@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS, cart_count=cart_count())


@app.route('/cart')
def cart():
    items, total = cart_details()
    return render_template('cart.html', items=items, total=total)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    items, total = cart_details()
    if request.method == 'POST':
        # Simple demo: collect form and clear cart
        customer = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'address': request.form.get('address'),
            'payment': request.form.get('payment')
        }
        session.pop('cart', None)
        return render_template('order_confirm.html', customer=customer, items=items, total=total)
    return render_template('checkout.html', items=items, total=total)


@app.route('/api/cart', methods=['GET'])
def api_cart():
    items, total = cart_details()
    qty = cart_count()
    simple_items = [{'id': it['product']['id'], 'name': it['product']['name'], 'qty': it['qty'], 'subtotal': it['subtotal']} for it in items]
    return jsonify({'items': simple_items, 'total': total, 'qty': qty})


@app.route('/api/add', methods=['POST'])
def api_add():
    data = request.get_json() or request.form
    pid = data.get('product_id')
    if not pid:
        return jsonify({'error': 'missing product_id'}), 400
    p = find_product(pid)
    if not p:
        return jsonify({'error': 'invalid product_id'}), 404
    cart = get_cart()
    cart[str(p['id'])] = cart.get(str(p['id']), 0) + 1
    session['cart'] = cart
    return jsonify({'qty': cart_count()})


@app.route('/api/update', methods=['POST'])
def api_update():
    data = request.get_json() or request.form
    pid = data.get('product_id')
    qty = int(data.get('qty', 0))
    cart = get_cart()
    if pid and str(pid) in cart:
        if qty <= 0:
            cart.pop(str(pid), None)
        else:
            cart[str(pid)] = qty
        session['cart'] = cart
    items, total = cart_details()
    return jsonify({'items': len(items), 'total': total, 'qty': cart_count()})


@app.route('/api/remove', methods=['POST'])
def api_remove():
    data = request.get_json() or request.form
    pid = data.get('product_id')
    cart = get_cart()
    cart.pop(str(pid), None)
    session['cart'] = cart
    return jsonify({'qty': cart_count()})


if __name__ == '__main__':
    app.run(debug=True)
