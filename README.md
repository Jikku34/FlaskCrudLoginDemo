
Flask Product and User Management Application Setup Guide

This document provides detailed instructions to help you set up and run the Flask Product and User Management Application.

Prerequisites
Before setting up and running the application, ensure the following are installed on your system:

1. Python 3.x: Download from https://www.python.org/downloads/
2. MySQL: Download from https://dev.mysql.com/downloads/installer/
3. Git: Download and install from https://git-scm.com/downloads
4. Text Editor or IDE: Such as Visual Studio Code, PyCharm, or Sublime Text.

Project Overview
The application provides the following features:

- Product Management: You can add, update, and delete products from the database.
- User Authentication: Users can log in and log out. Authentication is handled through session management.
- Database Integration: SQLAlchemy is used to interact with a MySQL database.
- Database Migrations: Flask-Migrate is used for schema migrations.

Technology Stack:
- Backend Framework: Flask (Python)
- Database: MySQL
- ORM: SQLAlchemy
- Database Migrations: Flask-Migrate
- Templating: Jinja2 (with HTML templates)

Getting Started
To set up and run this project on your local machine, follow the steps below.

1. Clone the Repository
Open a terminal or command prompt and run:

git clone https://github.com/yourusername/FlaskCrudLoginDemo.git
cd FlaskCrudLoginDemo

2. Set Up a Virtual Environment (Recommended)
It is a best practice to create a virtual environment to manage project dependencies.

On Windows:
python -m venv .venv
.venv\Scripts\activate

On MacOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

Once activated, your terminal will show (.venv) indicating the virtual environment is active.

3. Install Dependencies
Now, install the required Python packages by running:

pip install -r requirements.txt

Database Setup
The application uses MySQL as the database backend. Follow these steps to set up the database.

1. Create a MySQL Database
Open MySQL Workbench or use the command line to create a new MySQL database:

CREATE DATABASE demo_product;

Ensure that the database connection settings in app.py match your local setup.

2. Initialize and Migrate the Database
Once the database is set up, you need to initialize and apply the initial migration. Run the following commands:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Running the Application
After setting up the environment and database, you can now run the Flask application.

1. Start the Flask Development Server
To start the application, run the following command:

python app.py

You will see output similar to this:

* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Visit http://127.0.0.1:5000/ in your web browser to view the app.

2. Stop the Server
To stop the server, press CTRL+C in the terminal window where the server is running.

Usage
Here’s how you can use the various features of the application:

1. Homepage (/)
- Displays all the products available in the database.

2. Add Product (/add)
- Allows you to add a new product by filling out the form with product details.

3. Update Product (/update_product/<product_id>)
- Edit the details of a product by providing the product ID in the URL.

4. Delete Product (/delete/<product_id>)
- Deletes a product from the database based on the provided product ID.

5. User Login (/login)
- Login with a username and password to authenticate.

6. Logout (/logout)
- Logs the user out by clearing the session.

7. About Page (/about)
- A protected page that can only be accessed if logged in.

8. Contact Page (/contact)
- A simple contact page.

Project Structure
Here’s the project folder structure:

├── app.py                 # Main Flask application file
├── migrations             # Flask-Migrate files for database migrations
├── requirements.txt       # Python package dependencies
├── templates              # HTML files (Jinja2 templates)
│   ├── index.html         # Homepage template
│   ├── add_product.html   # Add product template
│   ├── update_product.html # Update product template
│   ├── login.html         # Login template
│   ├── about.html         # About page template
│   └── contact.html       # Contact page template
├── README.md              # Project documentation

Troubleshooting
Here are some common issues and solutions:

1. Flask is not recognized as a command:
- Ensure Flask is installed by running pip install flask.

2. MySQL connection error:
- Ensure your MySQL service is running.
- Check that the credentials in app.config['SQLALCHEMY_DATABASE_URI'] are correct.

3. Page not loading or application error:
- Restart the Flask development server by pressing CTRL+C and running python app.py again.
- Check the terminal output for any error messages.

4. Migrations not working:
- Ensure that the migrations/ folder exists and that you have run flask db init to initialize the migration directory.

License
This project is open-source and available under the MIT License.
