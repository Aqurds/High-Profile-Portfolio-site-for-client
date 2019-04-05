from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import smtplib
import imghdr
from email.message import EmailMessage



app = Flask(__name__)



# Email sending function
def send_email(message, user_email):
    # EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    # EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    EMAIL_ADDRESS =  "leaddealing@gmail.com"
    EMAIL_PASSWORD = "Allah@DoYa@@KoRuN@@@"

    contacts = ['YourAddress@gmail.com', 'test@example.com']

    msg = EmailMessage()
    msg['Subject'] = 'Email from JacobsEdo.com'
    msg['From'] = user_email
    msg['To'] = 'omarf1320@gmail.com'

    # msg.set_content(message)

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <p style="color:SlateGray;">""" + message + """</p>
            <p style="color:red;">Email from: """ + user_email + """
        </body>
    </html>
    """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)




# Home route
@app.route('/')
def home():
    return render_template('index.html')



# About route
@app.route('/about/')
def about():
    return render_template('about.html')



# Speaking route
@app.route('/speaking/')
def speaking():
    return render_template('speaking.html')



# Book route
@app.route('/book/')
def book():
    return render_template('book.html')



# blog route
@app.route('/blog/')
def blog():
    return render_template('blog.html')



# Single blog route
@app.route('/single-blog/')
def single_blog():
    return render_template('single-blog.html')



# Contact route
@app.route('/contact/')
def contact():
    return render_template('contact.html')




# Admin route
@app.route('/admin/')
def admin():
    return render_template('admin.html')




# Privacy route
@app.route('/privacy/')
def privacy():
    return render_template('privacy.html')



# Contact form AJAX call process route
@app.route('/process', methods=['POST'])
def process():
    email = request.form['email']
    name = request.form['name']
    message = request.form['message']

    if name and email:
        if message:
            send_email(message, email)
            return jsonify({'feedback' : "Message Sent! Thanks!"})

    return jsonify({'error': 'Please fill the required fields!'})





if __name__ == '__main__':
    app.run(debug = True)
