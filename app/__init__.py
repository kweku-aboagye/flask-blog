import os
from flask import Flask, render_template, send_from_directory
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html', title="Firstname Lastname", url=os.getenv("URL"))

@app.route('/contact')
def contact():
    return render_template('contacts.html', title="Contact", url=os.getenv("URL"))

@app.route('/blog')
def blog():
    return render_template('blog.html', title="Blog", url=os.getenv("URL"))

@app.route('/projects')
def projects():
    return render_template('projects.html', title="Projects", url=os.getenv("URL"))