from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging
import sys
from models import db, Product, User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from applicationinsights.flask.ext import AppInsights

app = Flask(__name__)
# Add the following lines to configure logging to print debug messages
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)
appinsights = AppInsights(app)

# force flushing application insights handler after each request
@app.after_request
def after_request(response):
    appinsights.flush()
    return response
    
app.secret_key = 'your_secret_key'  # Change this to a secure, random key in a production environment
admins = {'admin': 'admin_password'}  # Add your admin credentials here
#app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://jz20000cn:'820916Yg!'@nodaldata.database.windows.net/Nodal?driver=ODBC+Driver+18+for+SQL+Server"
app.config['SQLALCHEMY_DATABASE_USERNAME'] = 'jz20000cn'
app.config['SQLALCHEMY_DATABASE_PASSWORD'] = '820916Yg!'
app.config['SQLALCHEMY_DATABASE_SERVER'] = 'nodaldata.database.windows.net'
app.config['SQLALCHEMY_DATABASE_NAME'] = 'Nodal'
app.config['SQLALCHEMY_DATABASE_DRIVER'] = 'ODBC+Driver+18+for+SQL+Server'
app.config['SQLALCHEMY_BINDS'] = {
    None: "mssql+pyodbc://jz20000cn:820916Yg!@nodaldata.database.windows.net/Nodal?driver=ODBC+Driver+18+for+SQL+Server&login_timeout=30"
}
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://jz20000cn:820916Yg!@nodaldata.database.windows.net/Nodal?driver=ODBC+Driver+18+for+SQL+Server&login_timeout=30"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour (in seconds)
#db = SQLAlchemy(app)
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager(app)


# Mock user class for demonstration purposes
#class User(UserMixin):
   # def __init__(self, user_id, username, password, role):
   #     self.id = user_id
    #    self.username = username
    #    self.password = password
     #   self.role = role

# Mock user database for demonstration purposes
#users = {
 #   1: User(1, 'admin', 'admin_password', 'admin'),
#}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Data structures to store visitor information
all_visitors = []
question_submissions = []

# Function to check if the user is logged in as an admin
def is_admin():
    return session.get('username') in admins

# Home route
@app.route('/')
def home():
    try:
        # Capture visitor information
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        visitor_info = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip_address': client_ip,
            'user_agent': request.user_agent.string
        }
        all_visitors.append(visitor_info)

        return render_template('index.html')

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Form submission route
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')

    # Capture visitor information for question submissions
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    visitor_info = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip_address': client_ip,
        'user_agent': request.user_agent.string
    }
    all_visitors.append(visitor_info)

    # Process the form data (you can add your own logic here)
    if name and email and subject:
        question_data = {
            'timestamp': visitor_info['timestamp'],
            'ip_address': visitor_info['ip_address'],
            'user_agent': visitor_info['user_agent'],
            'name': name,
            'email': email,
            'subject': subject
        }
        question_submissions.append(question_data)

    return f'Thank you, {name}! Your email ({email}) regarding "{subject}" has been submitted.'

# Mock admin credentials (temporary)
admins = {'admin': 'admin_password'}

# ... (other routes and configurations)

# Update the 'admin_login' route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            app.logger.debug(f"Attempting to log in as {username}")

            # Check if provided credentials match the admin credentials
            if username in admins and admins[username] == password:
                app.logger.debug(f"Login successful for {username}")

                # Store admin information in the session
                session['username'] = username
                session['is_admin'] = True

                app.logger.debug(f"Session information: {session}")

                # For additional debugging, print the headers and form data
                app.logger.debug(f"Request headers: {request.headers}")
                app.logger.debug(f"Form data: {request.form}")

                return redirect(url_for('admin_dashboard'))

            app.logger.debug(f"Login failed for {username}")

        app.logger.debug("Rendering admin login page")
        return render_template('admin_login.html')

    except Exception as e:
        # Log the exception details
        app.logger.exception("Error during admin login:")
        return f"An error occurred during admin login: {str(e)}", 500


# Admin dashboard route
@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('admin_login'))
    products = Product.query.all()
    return render_template('admin_dashboard.html', all_visitors=all_visitors, question_submissions=question_submissions, products=products)

# Admin logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin_login'))


# Products route
@app.route('/products')
def products():
    # Your products page logic goes here
    return render_template('products.html')



# Products form submission route
@app.route('/submit_product_form', methods=['POST'])
def submit_product_form():
    try:
        name = request.form.get('name')
        address = request.form.get('address')
        energy_usage = float(request.form.get('energy_usage'))
        num_cars = int(request.form.get('num_cars'))
        energy_storage = float(request.form.get('energy_storage'))

        # Save the product to the database
        new_product = Product(name=name, address=address, energy_usage=energy_usage, num_cars=num_cars, energy_storage=energy_storage)
        db.session.add(new_product)
        db.session.commit()

        return render_template('product_submission_success.html', name=name)

    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback changes to avoid leaving the database in an inconsistent state
        error_message = f"Database error: {str(e)}"
        connection_details = get_connection_details()
        return render_template('product_submission_error.html', error_message=error_message, connection_details=connection_details)

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_template('product_submission_error.html', error_message=error_message)


def get_connection_details():
    """
    Get relevant information from the configuration.
    """
    connection_details = {
        'username': app.config.get('SQLALCHEMY_DATABASE_USERNAME'),
        'password': app.config.get('SQLALCHEMY_DATABASE_PASSWORD'),
        'server': app.config.get('SQLALCHEMY_DATABASE_SERVER'),
        'database': app.config.get('SQLALCHEMY_DATABASE_NAME'),
        'driver': app.config.get('SQLALCHEMY_DATABASE_DRIVER'),
    }

    return connection_details


@app.errorhandler(500)
def internal_server_error(e):
    app.logger.exception("Internal Server Error:")
    return f"Internal Server Error: {str(e)}", 500
    
if __name__ == '__main__':
    app.run(debug=True)
