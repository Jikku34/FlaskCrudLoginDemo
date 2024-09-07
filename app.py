"""
This script initializes a Flask application with SQLAlchemy and Flask-Migrate for database operations and migrations.

Modules:
    - Flask: The main framework to create a web application.
    - render_template: To render HTML templates.
    - request: To handle HTTP requests.
    - redirect: To redirect to other routes.
    - session: To manage user sessions.
    - SQLAlchemy: To handle ORM (Object Relational Mapping) and interact with the database.
    - Migrate: To handle database migrations (changes to the database schema).

Configuration:
    - SQLALCHEMY_DATABASE_URI: Connects to the MySQL database 'demo_product' with the root user.
    - SQLALCHEMY_TRACK_MODIFICATIONS: Disables tracking of object modifications to save resources.
    - secret_key: A key used for managing the user session securely.

Components:
    - db: Instance of SQLAlchemy, used for interacting with the database (querying, creating, updating, and deleting records).
    - migrate: Instance of Migrate, used to apply database migrations.
"""

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
    """
    Represents the product table in the database.

    Columns:
        - id (Integer): The primary key for the product.
        - name (String): The name of the product.
        - price (Float): The price of the product.
        - category (String): The category to which the product belongs.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    category = db.Column(db.String(100))


class UserModel(db.Model):
    """
    Represents the user table in the database.

    Columns:
        - username (String): The username for the user (primary key).
        - user_password (String): The password for the user (hashed).
        - user_email (String): The email address of the user.
    """
    username = db.Column(db.String(200), primary_key=True)
    user_password = db.Column(db.String(300))
    user_email = db.Column(db.String(300))


@app.route('/')
def home():
    """
    Renders the homepage with a list of all products.

    Fetches all products from the database and passes them to the template 'index.html'.
    If there are no products in the database, an empty list will be passed.

    Returns:
        Rendered HTML page with the list of products.
    """
    products = ProductModel.query.all()  # Query all products from the database
    return render_template('index.html', my_products=products)


@app.route('/about')
def about():
    """
    Renders the 'About' page.

    If the user is logged in (checked through session), the 'about.html' page is displayed.
    Otherwise, the user is redirected to the login page.

    Returns:
        Rendered HTML page for the 'About' section or a redirect to the login page.
    """
    if 'user' in session:
        return render_template('about.html')
    else:
        return redirect('/login')


@app.route('/contact')
def contact():
    """
    Renders the 'Contact' page.

    Simply renders the 'contact.html' page without any data manipulation.

    Returns:
        Rendered HTML page for the 'Contact' section.
    """
    return render_template('contact.html')


@app.route('/add', methods=['GET', "POST"])
def add_product():
    """
    Handles the addition of a new product.

    For GET requests:
        - Renders the 'add_product.html' template with a form to add a new product.

    For POST requests:
        - Retrieves form data (product details) from the request.
        - Creates a new ProductModel instance.
        - Adds and commits the new product to the database.
        - Redirects to the homepage after successful addition.

    Returns:
        - GET: Rendered HTML form for adding a new product.
        - POST: Redirect to the homepage after adding the product.
    """
    if request.method == "POST":
        # Get form data from the request
        product_id = int(request.form['id'])
        product_name = request.form['name']
        product_price = float(request.form['price'])
        product_category = request.form['category']

        # Create a new product object and save it to the database
        product_obj = ProductModel(id=product_id, name=product_name, price=product_price, category=product_category)
        db.session.add(product_obj)
        db.session.commit()

        return redirect('/')

    return render_template('add_product.html')


@app.route('/product/<int:product_id>')
def product(product_id):
    """
    Displays the product ID.

    This route simply takes a product ID as input and returns it as a string.
    Primarily used for debugging or showing basic information.

    Args:
        product_id (int): The ID of the product passed in the URL.

    Returns:
        A string displaying the product ID.
    """
    return f'id of product is : {product_id}'


@app.route('/update_product/<int:product_id>', methods=['POST', "GET"])
def update_product(product_id):
    """
    Updates the details of an existing product.

    For GET requests:
        - Fetches the product by its ID and renders the 'update_product.html' form pre-filled with the product's data.

    For POST requests:
        - Updates the product details (name, price, category) based on the form input.
        - Commits the changes to the database and redirects to the homepage.

    Args:
        product_id (int): The ID of the product to update.

    Returns:
        - GET: Rendered HTML form with pre-filled product data for updating.
        - POST: Redirect to the homepage after updating the product.
    """
    product = ProductModel.query.get(product_id)  # Find product by ID

    if request.method == 'POST':
        # Update product details
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.category = request.form['category']

        db.session.commit()
        return redirect('/')

    return render_template('update_product.html', product=product)


@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    """
    Deletes a product by its ID.

    This function deletes a product from the database using the product ID provided in the URL.
    After deleting, it redirects to the homepage.

    Args:
        product_id (int): The ID of the product to delete.

    Returns:
        Redirect to the homepage after deletion.
    """
    product = ProductModel.query.get(product_id)  # Find the product by ID
    if product:
        db.session.delete(product)
        db.session.commit()

    return redirect('/')


@app.route('/login', methods=['POST', "GET"])
def login():
    """
    Handles user login.

    For GET requests:
        - Renders the 'login.html' template with a form for user login.

    For POST requests:
        - Retrieves the username and password from the form data.
        - Checks if a user with the provided credentials exists in the database.
        - If the user exists, they are logged in (session is created), and redirected to the homepage.
        - If the credentials are invalid, an 'Invalid Credentials' message is shown.

    Returns:
        - GET: Rendered HTML form for user login.
        - POST: Redirect to the homepage if login is successful or a message if credentials are invalid.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists with the provided credentials
        user = UserModel.query.filter_by(username=username, user_password=password).first()
        if user:
            session['user'] = username  # Set user session
            return redirect('/')
        else:
            return 'Invalid Credentials'

    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    Logs out the current user.

    Clears the user session and redirects to the homepage.

    Returns:
        Redirect to the homepage after logging out.
    """
    session.pop('user', None)  # Remove the user session
    return redirect('/')


"""
This block ensures that the Flask application runs only when the script is executed directly (not when imported as a module).

The Flask `app.run()` method starts the development server with the following options:
    - debug=True: Enables debug mode, which provides detailed error messages and automatically reloads the server when code changes.

When this script is run, the Flask application will start, allowing it to handle incoming HTTP requests.
"""

if __name__ == '__main__':
    app.run(debug=True)
