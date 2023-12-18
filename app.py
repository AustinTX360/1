from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure, random key in a production environment
admins = {'admin': 'admin_password'}  # Add your admin credentials here

# Function to check if the user is logged in as an admin
def is_admin():
    return session.get('username') in admins

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

# Admin logout route
@app.route('/admin/logout')
def admin_logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
