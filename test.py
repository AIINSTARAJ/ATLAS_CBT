from flask import Flask, redirect, render_template,request,flash,url_for 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.sql import func 
import os
from flask_mail import Mail, Message
import webbrowser

#webbrowser.open("http://127.0.0.1:5000", 1)

app = Flask(__name__,template_folder="TEMPLATES")

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir,'data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tomiwakuteyi@gmail.com'
app.config['MAIL_PASSWORD'] = 'Abhishek12$'

mail = Mail(app)

db = SQLAlchemy(app)

class BOOK(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    Author = db.Column(db.String(25),nullable = False)
    Publisher = db.Column(db.String(25),nullable = False)
    mail = db.Column(db.String(9-25),nullable = False)
    Title = db.Column(db.String(50),nullable = False)
    Brief = db.Column(db.Text(120-500),nullable = False)
    Icon = db.Column(db.String(255),nullable = False)
    Book = db.Column(db.String(255), nullable=False)
    year = db.Column(db.SMALLINT,nullable = False)
    date = db.Column(db.DateTime(timezone=True), server_default = func.now())
    Categories = db.Column(db.String,nullable = False)

    def __repr__(self):
        return f'<BOOK {self.Title}>'
    

@app.route('/')
def index():
    books = BOOK.query.order_by(BOOK.date).all()
    return render_template('index.html',Books = books)


@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/<categories>/')
def categories(categories):
    return None
    #BOOK_CATEGORY = BOOK.query_by(categories).all()


@app.route('/add_book/', methods = ('GET','POST'))
def add_book():
    if request.method == 'POST':
        Author = request.form['author']
        Publisher = request.form['publisher']
        mail = request.form['mail']
        Title = request.form['title']
        Brief = request.form['brief']
        Icon = request.files['icon']
        Book = request.files['book']
        year = request.form['year']
        #date = request.form['date']
        Categories = request.form['categories']
        if Icon:
            Icon_name = Icon.filename
            Icon.save(os.path.join(app.config['UPLOAD_FOLDER'], Icon_name))
        if Book:
            Book_name = Book.filename
            Book.save(os.path.join(app.config['UPLOAD_FOLDER'],Book_name))
        new_book = BOOK(Author = Author,Publisher = Publisher,mail=mail,Title=Title,Brief= Brief,Icon=Icon_name,
                        Book = Book_name,year=year,Categories= Categories)

        db.session.add(new_book)
        db.session.commit()
        try:
            send_email()
        except:
            return "ERROR"

        return redirect(url_for('index'))
    
    return render_template('add_book.html')

def send_email():
    msg = Message('Hello', sender='tomiwakuteyi@gmail.com', recipients= BOOK.mail)
    msg.body = "This is a test email sent from X-Books for sucessfully signing up on X-BOOKS."
    mail.send(msg)
    return "Email sent successfully"

if __name__ == '__main__':
    app.run(debug = True)
    
