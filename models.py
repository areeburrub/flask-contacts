from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
from datetime import datetime

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:flaskuser@localhost/flask_contacts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):


    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True, unique=False)

    def __repr__(self):
        return '<Contacts %r>' % self.name

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.String(15), nullable = False)
    to = db.Column(db.String(80), nullable = False)
    text = db.Column(db.String(15), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)