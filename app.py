from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure, random key in a production environment
admins = {'admin': 'admin_password'}  # Add your admin credentials here

# Data structure to store visitor information
visitors = []

# Function to check if the user is logged in as an admin
def is_admin():
    return session.get('username') in admins

# Home route
@app.route('/')
def home():
    # Capture visitor information
    visitor_info = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip_address': request.remote_addr,
        'user_agent': request.user_agent.string
    }
    visitors.append(visitor_info)

    return render_template('index.html')

# ... (other routes)

# Admin dashboard route
@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('admin_login'))

    return render_template('admin_dashboard.html', visitors=visitors)

# ... (other routes)

if __name__ == '__main__':
    app.run(debug=True)
In this example:

The visitors list stores dictionaries with information about each visitor, including the timestamp, IP address, and user agent.
The home route captures visitor information and appends it to the visitors list.
Please note that this is a basic example, and in a production environment, you might want to store this data in a more persistent and scalable way, such as using a database.

Additionally, capturing visitor information in this manner might not work as expected if your application is behind a reverse proxy or load balancer. In such cases, you might need to configure your server to handle the correct IP address.




User
can you include everything we talked about in one app.py?
ChatGPT
Certainly! Below is an updated version of your app.py file that includes all the discussed features:

python
Copy code
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure, random key in a production environment
admins = {'admin': 'admin_password'}  # Add your admin credentials here

# Data structure to store visitor information
visitors = []

# Function to check if the user is logged in as an admin
def is_admin():
    return session.get('username') in admins

# Home route
@app.route('/')
def home():
    # Capture visitor information
    visitor_info = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip_address': request.remote_addr,
        'user_agent': request.user_agent.string
    }
    visitors.append(visitor_info)

    return render_template('index.html')

# Form submission route
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    
    # Process the form data (you can add your own logic here)
    
    return f'Thank you, {name}! Your email ({email}) regarding "{subject}" has been submitted.'

# Contact form submission route
@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # Process the contact form data (you can add your own logic here)
    
    return f'Thank you, {name}! Your email ({email}) with the message "{message}" has been submitted.'

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

    return render_template('admin_dashboard.html', visitors=visitors)

# Admin logout route
@app.route('/admin/logout')
def admin_logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
