import os
from flask import Flask, render_template, send_from_directory, redirect, url_for, session, request
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import smtplib
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}'.format(
    user=os.getenv('POSTGRES_USER'),
    passwd=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=5432,
    table=os.getenv('POSTGRES_DB'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)


class PostForm(FlaskForm):
    body = TextAreaField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserModel(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


@app.route('/')
def index():
    return render_template('index.html', title="Firstname Lastname", url=os.getenv("URL"))


@app.route('/contact')
def contact():
	
    return render_template('contacts.html', title="Contact", url=os.getenv("URL"))

@app.route('/form',methods=["POST"])
def form():
	name = request.form.get("name")
	email = request.form.get("email")
	msg = request.form.get("msg")
	
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login("[REDACTED_EMAIL]", os.getenv("PASS"))
	server.sendmail("[REDACTED_EMAIL]", "[REDACTED_EMAIL]", name+" "+email+" "+msg)
	
	return render_template("form.html", title="Form",na=name, em=email, mens=msg)

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    form = PostForm()
    if form.validate_on_submit():
        session['post'] = form.body.data
        return redirect(url_for('blog'))
    return render_template('blog.html', title="Blog", url=os.getenv("URL"), form=form, post=session.get('post'))


@app.route('/projects')
def projects():
	# Hardcoded projects names
	robotics_projects = ['Sumo Robot/sumo.jpg', 'Line Following Robot/line_follower.png', 'Soccer Robot/soccer_robot.jpeg', 'Fire Extinguishing Robot/fire_robot.jpg']
	electronics_projects = ['Cell Phone Detector/Cell-phone-detector.jpg', 'Mobile Jammer Circuit/Mobile-Jammer.jpg']
	ai_projects = ['Font Classifier Perceptron/robot_img_example.png']
	misc_projects = ['Snake Video Game/snake.png']
	projects_names = [robotics_projects, electronics_projects, ai_projects, misc_projects]
	
	page = request.args.get('page')
	if page and page.isdigit():
		page = int(page)
	else:
		page = 1
	
	return render_template('projects.html', title="Projects", url=os.getenv("URL"), projects=projects_names,pag = page)


@app.route('/health', methods=['GET'])
def health():
	return "Works"

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return f"User {username} created successfully"
        else:
            return error, 418

    ## TODO: Return a restister page
    return "Register Page not yet implemented", 501

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            return "Login Successful", 200 
        else:
            return error, 418
    
    ## TODO: Return a login page
    return "Login Page not yet implemented", 501