from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    
    # Process the form data (you can add your own logic here)
    
    return f'Thank you, {name}! Your email ({email}) regarding "{subject}" has been submitted.'

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # Process the contact form data (you can add your own logic here)
    
    return f'Thank you, {name}! Your email ({email}) with the message "{message}" has been submitted.'

if __name__ == '__main__':
    app.run(debug=True)
