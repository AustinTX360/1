from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import logging
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure, random key in a production environment
admins = {'admin': 'admin_password'}  # Add your admin credentials here

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

if __name__ == '__main__':
    app.run(debug=True)
