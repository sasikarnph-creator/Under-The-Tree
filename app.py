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
    {"id": 7, "name": "Eternal Spring", "category": "โรแมนติก", "price": 13.99, "image": "static/images/product7.svg", "desc": "เรื่องรักที่เกิดขึ้นในสวนสวรรค์ต่างโลก"},
    {"id": 8, "name": "The Crystal Shadow", "category": "แฟนตาซี", "price": 15.50, "image": "static/images/product8.svg", "desc": "ศึกษาเพื่อค้นหาอำนาจลี้ลับของคริสตัลวิเศษ"},
    {"id": 9, "name": "Mystery of the Old Tower", "category": "นิยายสืบสวน", "price": 10.99, "image": "static/images/product9.svg", "desc": "ป้อมเก่าแзакซ้อนความลึกลับที่ยังไม่มีใครรู้"},
    {"id": 10, "name": "Beyond the Horizon", "category": "แฟนตาซี", "price": 17.25, "image": "static/images/product10.svg", "desc": "เสาร์ขสำรวจไปยังเทพภูมิที่ลึกลับ"},
    {"id": 11, "name": "Autumn Whispers", "category": "โรแมนติก", "price": 11.50, "image": "static/images/product11.svg", "desc": "ความรักที่เบาบางเหมือนใบไม้ร่วงในฤดูใบไม้ร่วง"},
    {"id": 12, "name": "The Invisible Thief", "category": "นิยายสืบสวน", "price": 12.75, "image": "static/images/product12.svg", "desc": "การไล่ตามโจรลี้ลับที่ไม่มีใครเห็นหน้า"},
    {"id": 13, "name": "Dragon's Realm", "category": "แฟนตาซี", "price": 18.99, "image": "static/images/product13.svg", "desc": "มหากาพย์แห่งพระมังกรและอาณาจักรวิเศษ"},
    {"id": 14, "name": "Second Chance", "category": "โรแมนติก", "price": 10.50, "image": "static/images/product14.svg", "desc": "โอกาสสองครั้งของความรักที่เก่าแก่"},
    {"id": 15, "name": "The Coded Message", "category": "นิยายสืบสวน", "price": 14.99, "image": "static/images/product15.svg", "desc": "รหัสลับที่จะเปิดเผยความจริงของโลก"},
    {"id": 16, "name": "Sacred Woods", "category": "แฟนตาซี", "price": 16.25, "image": "static/images/product16.svg", "desc": "ป่าศักดิ์สิทธิ์ที่บ้านของจิตวิญญาณ"},
    {"id": 17, "name": "Love in Winter", "category": "โรแมนติก", "price": 12.50, "image": "static/images/product17.svg", "desc": "ความหนาวเย็นของฤดูหนาวแต่ใจอบอุ่น"},
    {"id": 18, "name": "Lost in Time", "category": "นิยายสืบสวน", "price": 15.75, "image": "static/images/product18.svg", "desc": "หายลงในกระแสเวลา ค้นหาวิธีกลับบ้าน"},
]


import sqlite3
from flask import g

DB_PATH = 'data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            image TEXT,
            desc TEXT
        )
    ''')
    conn.commit()

    # If DB empty, seed from in-memory PRODUCTS
    c.execute('SELECT COUNT(*) as cnt FROM products')
    row = c.fetchone()
    if row and row[0] == 0:
        for p in PRODUCTS:
            c.execute('INSERT INTO products (name, category, price, image, desc) VALUES (?,?,?,?,?)',
                      (p.get('name'), p.get('category'), p.get('price'), p.get('image'), p.get('desc')))
        conn.commit()
    conn.close()

def load_products_from_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute('SELECT id, name, category, price, image, desc FROM products ORDER BY id')
    rows = cur.fetchall()
    db.close()
    prods = []
    for r in rows:
        prods.append({'id': r['id'], 'name': r['name'], 'category': r['category'], 'price': r['price'], 'image': r['image'], 'desc': r['desc']})
    return prods

# initialize DB and load products to in-memory list used by routes
init_db()
PRODUCTS = load_products_from_db()
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


@app.route('/product/<int:pid>')
def product_detail(pid):
    p = find_product(pid)
    if not p:
        return "Product not found", 404
    return render_template('product_detail.html', product=p, cart_count=cart_count())


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


# --- Admin (simple) ---
def require_admin(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('login', next=request.path))
        return fn(*args, **kwargs)
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == '1234':
            session['is_admin'] = True
            next_url = request.args.get('next') or url_for('admin')
            return redirect(next_url)
        else:
            return render_template('login.html', error='ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))


@app.route('/admin')
@require_admin
def admin():
    prods = load_products_from_db()
    return render_template('admin.html', products=prods)


@app.route('/admin/add', methods=['POST'])
@require_admin
def admin_add():
    name = request.form.get('name')
    price = request.form.get('price')
    image = request.form.get('image')
    category = request.form.get('category') or ''
    desc = request.form.get('desc') or ''
    try:
        price_f = float(price)
    except (TypeError, ValueError):
        price_f = 0.0
    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO products (name, category, price, image, desc) VALUES (?,?,?,?,?)',
                (name, category, price_f, image, desc))
    db.commit()
    return redirect(url_for('admin'))


@app.route('/admin/delete/<int:pid>', methods=['POST'])
@require_admin
def admin_delete(pid):
    db = get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM products WHERE id = ?', (pid,))
    db.commit()
    return redirect(url_for('admin'))


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
