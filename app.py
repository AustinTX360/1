from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging
import sys

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.secret_key = 'your_secret_key'  # Change this to a secure, random key in a production environment
admins = {'admin': 'admin_password'}  # Add your admin credentials here
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://jz20000cn:'820916Yg!'@nodaldata.database.windows.net/Nodal?driver=ODBC+Driver+17+for+SQL+Server"
db = SQLAlchemy(app)

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

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in admins and admins[username] == password:
            session['username'] = username
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

# Admin dashboard route
@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('admin_login'))

    return render_template('admin_dashboard.html', all_visitors=all_visitors, question_submissions=question_submissions)

# Admin logout route
@app.route('/admin/logout')
def admin_logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# Enable logging to the console
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

# Products route
@app.route('/products')
def products():
    # Your products page logic goes here
    return render_template('products.html')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    energy_usage = db.Column(db.Float, nullable=False)
    num_cars = db.Column(db.Integer, nullable=False)
    energy_storage = db.Column(db.Float, nullable=False)

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
    Get relevant information from the connection string.
    """
    connection_string = app.config.get('SQLALCHEMY_DATABASE_URI', '')

    # Log the connection string
    app.logger.debug(f"Connection String: {connection_string}")

    return {'connection_string': connection_string}
    
if __name__ == '__main__':
    app.run(debug=True)
