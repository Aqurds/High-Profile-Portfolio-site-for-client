from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import smtplib
import imghdr
from email.message import EmailMessage
import pymongo
import urllib


# MongoDB Atlas connection
mongo = pymongo.MongoClient('mongodb+srv://jacobs:' + urllib.parse.quote_plus('Y5oyE2EDxAQJdw53') + '@cluster0-xpfof.mongodb.net/test?retryWrites=true', maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, 'edoblog')




app = Flask(__name__)
app.config['SECRET_KEY'] = '0f9dc56d2288afa6e10b8d97577fe25b'



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

    # Fetching the database for all blog post
    col = pymongo.collection.Collection(db, 'blog_post')
    blog_posts = list(col.find())

    return render_template('blog.html', blog_posts=blog_posts)



# Single blog route
@app.route('/post/')
def post():
    post_title_as_id = request.args.get('post_id')

    # Fetching the database for all blog post
    col = pymongo.collection.Collection(db, 'blog_post')
    single_post = list(col.find({'title': post_title_as_id}))
    all_post = list(col.find())
    index_of_current_post = 0
    for post in all_post:
        if post['title'] == post_title_as_id:
            index_of_current_post = all_post.index(post)

    del all_post[index_of_current_post]

    # Fetching comments from comment collection
    col = pymongo.collection.Collection(db, 'comments')
    comments = list(col.find({'title':post_title_as_id}))


    return render_template('post.html', post_title_as_id=post_title_as_id, single_post=single_post, all_post=all_post, comments=comments)



# Contact route
@app.route('/contact/')
def contact():
    return render_template('contact.html')




# Admin route
@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if session:
        file_name = ''

        if request.method == "POST":
            title = request.form['title']
            body = request.form['post_body']
            post_image = request.files['image']
            post_image_name = post_image.filename
            picture_path = os.path.join(app.root_path, 'static/img/blogimage', post_image_name)
            # file.save(os.path.join(image_folder, file_name))
            post_image.save(picture_path)
            col = pymongo.collection.Collection(db, 'blog_post')
            col.insert({'title':title, 'body':body, 'image':post_image_name})
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))




# Login route
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if session:
        return redirect(url_for('admin'))

    return render_template('login.html')




# Login form AJAX call process route
@app.route('/loginprocess', methods=['POST'])
def loginprocess():
    username = request.form['name']
    password = request.form['password']

    # Fetching the database for admin authentication
    col = pymongo.collection.Collection(db, 'jocobs')
    admin_user = list(col.find({'name' : username}))

    if admin_user:
        if password == admin_user[0]["password"]:
            session['username'] = username
            return redirect(url_for('admin'))
    else:
        return jsonify({'error': 'Invalid username or password!'})



# Login form AJAX call process route
@app.route('/commentprocess', methods=['POST'])
def commentprocess():
    username = request.form['name']
    email = request.form['email']
    comment = request.form['comment']
    title = request.form['title']
    data = {
    "name": username,
    "email": email,
    "comment": comment
    }

    # Inserting comment with title reference in comments collection
    col = pymongo.collection.Collection(db, 'comments')
    col.insert({"title": title, "comment": data})
    return jsonify({'feedback': 'Invalid username or password!'})





# Logout route
@app.route('/logout/')
def logout():
    if session:
        session.clear()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))




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




# Test route to test developement data
@app.route('/test/', methods=['GET', 'POST'])
def test():
    # APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    # target = os.path.join(APP_ROOT, 'static/img/blogimage')
    # image_folder = url_for('static', filename='img/blogimage')
    file_name = ''
    path = app.root_path

    if request.method == "POST":
        file = request.files['image']
        file_name = file.filename
        picture_path = os.path.join(app.root_path, 'static/img/blogimage', file_name)
        # file.save(os.path.join(image_folder, file_name))
        file.save(picture_path)


    return render_template('test.html', dir=path, file_name=file_name)



if __name__ == '__main__':
    app.run(debug = True)
