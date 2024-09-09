from flask import * 
from flask_sqlalchemy import * 
from werkzeug.security import * 
from sqlalchemy.sql import *
import time
import os
from hashlib import *
import webbrowser
"""

Importation of modules flask and other modules for functionality.

"""
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir,'info.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.getenv("secret-key")

db = SQLAlchemy(app)

#webbrowser.open("https://127.0.0.1:5000/")

class student(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(12),nullable = False)
    password = db.Column(db.String(128),nullable = False)
    mail = db.Column(db.String(48),nullable = False)
    date = db.Column(db.DateTime(timezone=True), server_default = func.now())

    def __repr__(self):
        return f'<student {self.username}>'
    
class result(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable = False)
    exam_name = db.Column(db.String(120),nullable = False)
    score = db.Column(db.Integer,nullable = False)
    student = db.relationship('student',backref = db.backref('result',lazy = True))
    
    def __repr__(self):
        return f'<result {self.exam_name}>'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/signup/', methods = ("GET","POST"))
def signup():
    a = session.get("name")
    b = session.get("mail")
    c = session.get("pwd")
    if a and b and c:
        time.sleep(2.4)
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            name = request.form['username']
            mail = request.form['mail']
            pwd = request.form['pwd']
            pwd = generate_password_hash(pwd,"scrypt",16)
            exist_user = student.query.filter_by(username = name).first()
            exist_mail = student.query.filter_by(mail=mail).first()
            if exist_user or exist_mail:
                flash("Username or e-mail address already exists. Please choose another username or e-mail!.","error")
                time.sleep(3.54)
                return redirect(url_for('signup'))
            else:
                new_user = student(username = name, mail = mail, password = pwd)
                db.session.add(new_user)
                db.session.commit()
                session['name'] = name
                session['mail'] = mail
                session['pwd'] = pwd
                flash("Signup Sucessful!.","sucess")
                time.sleep(2.4)
                return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login/',methods = ["GET","POST"])
def login():
    a = session.get("name")
    b = session.get("mail")
    c = session.get("pwd")
    if a and b and c:
        time.sleep(2.4)
        return redirect(url_for('exams'))
    else:
        if request.method == "POST":
            name = request.form["username"]
            mail = request.form['mail']
            pwd = request.form['pwd']
            user = student.query.filter_by(username = name).first()
            h = check_password_hash(user.password,pwd)
            if user and h:
                flash('Login Successful!','sucess')
                time.sleep(0.54)
                session['name'] = user.username
                session['mail'] = user.mail
                session['pwd'] = user.password
                return redirect(url_for("exams"))
            else:
                flash('Invalid Username or Password', 'error')
                time.sleep(0.64)
                return redirect(url_for("login"))
        return render_template('login.html')

def login_required(f):
    def decorated_function(*args,**kwargs):
        if 'name' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return decorated_function

def load_question(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        question:dict = json.load(file)
    return question

@app.route('/exams/',methods = ["GET","POST"])
def exams():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        user = session.get('name')
        User = student.query.filter_by(username = user).first()
        available_exams = ['CSC 101 - Introduction to Computing I', 'TPD 101 - Engineers in Society']
        return render_template('exams.html', exams = available_exams, username = User.username)


@app.route('/exam/<exam_name>', methods = ['GET','POST'])
def take_exam(exam_name):
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        exam_named = exam_name[:3] + '_' + exam_name[4:7]
        to_look_for = 'questions/' + exam_named + '.json'
        questions = load_question(to_look_for)
        if request.method == 'POST':
            current_question = int(request.form['current_question'])
            selected_option = request.form['option']
            if 'user_answers' not in session:
                session['user_answers'] = {}
            session['user_answers'][current_question] = selected_option
            session.modified = True
            if current_question < len(questions): 
                current_question += 1
                return redirect(url_for('take_exam',exam_name = exam_name, question = current_question))
            else:
                return redirect(url_for('submit_exam',exam_name = exam_name))
        current_question = int(request.args.get('current_question', 1))
        question = questions[current_question - 1]
        previous_answer = session.get(int('user_answers'), {}).get(current_question)
    return render_template(
        'exam.html',exam_name = exam_name,question = question, exam_named = exam_named,lenght = len(questions),previous_answer = previous_answer
        )



@login_required
@app.route('/submit_exam/<exam_name>')
def submit_exam(exam_name):
    exam_named = exam_name[:3] + '_' + exam_name[4:7]
    to_look_for = 'questions/' + exam_named + '.json'
    questions = load_question(to_look_for)
    score = 0
    for question in questions:
        if session['user_answers'].get(str(question['id'])) == question['answer']:
            score += 1
    Result = result(user_id = session['name'],exam_name = exam_name, score = score)
    db.session.add(Result)
    db.session.commit()
    session.pop('user_answers',None)
    return render_template('result.html',score = score,total = len(questions))
    
       
if __name__ == '__main__':
    app.run(debug = True)


