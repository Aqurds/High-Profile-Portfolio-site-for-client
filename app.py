from flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__)



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







if __name__ == '__main__':
    app.run(debug = True)
