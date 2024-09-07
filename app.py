from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/demo_product'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ASEDTRGGRCSDE'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class ProductModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    category = db.Column(db.String(100))


class UserModel(db.Model):
    username = db.Column(db.String(200), primary_key=True)
    user_password = db.Column(db.String(300))
    user_email = db.Column(db.String(300))


@app.route('/')
def home():
    products = ProductModel.query.all()
    # products = [
    #     {
    #         "id": 1,
    #         "name": "Laptop",
    #         "price": 750.00,
    #         "category": "Electronics",
    #         "in_stock": True
    #     },
    #     {
    #         "id": 2,
    #         "name": "Smartphone",
    #         "price": 500.00,
    #         "category": "Electronics",
    #         "in_stock": False
    #     },
    #     {
    #         "id": 3,
    #         "name": "Headphones",
    #         "price": 80.00,
    #         "category": "Accessories",
    #         "in_stock": True
    #     },
    #     {
    #         "id": 4,
    #         "name": "Keyboard",
    #         "price": 40.00,
    #         "category": "Accessories",
    #         "in_stock": True
    #     },
    #     {
    #         "id": 5,
    #         "name": "Monitor",
    #         "price": 200.00,
    #         "category": "Electronics",
    #         "in_stock": False
    #     },
    #     {
    #         "id": 6,
    #         "name": "Tablet",
    #         "price": 300.00,
    #         "category": "Electronics",
    #         "in_stock": True
    #     },
    #     {
    #         "id": 7,
    #         "name": "Backpack",
    #         "price": 60.00,
    #         "category": "Fashion",
    #         "in_stock": True
    #     },
    #     {
    #         "id": 8,
    #         "name": "Shoes",
    #         "price": 120.00,
    #         "category": "Fashion",
    #         "in_stock": False
    #     },
    #     {
    #         "id": 9,
    #         "name": "Water Bottle",
    #         "price": 15.00,
    #         "category": "Accessories",
    #         "in_stock": True
    #     },
    #     {
    #         "id": 10,
    #         "name": "Desk Chair",
    #         "price": 180.00,
    #         "category": "Furniture",
    #         "in_stock": True
    #     }
    # ]

    return render_template('index.html', my_products=products)


@app.route('/about')
def about():
    if 'user' in session:
        return render_template('about.html')
    else:
        return redirect('/login')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/add', methods=['GET', "POST"])
def add_product():
    print(request.method)
    if request.method == "POST":
        print("now method is POST")
        product_id = int(request.form['id'])
        product_name = request.form['name']
        product_price = float(request.form['price'])
        product_category = request.form['category']
        product_obj = ProductModel()
        product_obj.id = product_id
        product_obj.name = product_name
        product_obj.price = product_price
        product_obj.category = product_category
        db.session.add(product_obj)
        db.session.commit()
        return redirect('/')
    return render_template('add_product.html')


@app.route('/product/<int:product_id>')
def product(product_id):
    print(product_id)
    return f'id of product is : {product_id}'


@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    product = ProductModel.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/')


@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserModel.query.filter_by(username=username, user_password=password).first()
        if user:
            session['user'] = username
            return redirect('/')
        else:
            return 'Invalid Credentials'
    return render_template('login.html')


@app.route('/update_product/<int:product_id>', methods=['POST', "GET"])
def update_product(product_id):
    product = ProductModel.query.get(product_id)
    if request.method == 'POST':
        product_name = request.form['name']
        product_price = float(request.form['price'])
        product_category = request.form['category']
        product.name = product_name
        product.price = product_price
        product.category = product_category
        db.session.commit()
        return redirect('/')
    return render_template('update_product.html', product=product)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
