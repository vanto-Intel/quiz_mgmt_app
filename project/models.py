from enum import unique
from ssl import ALERT_DESCRIPTION_ACCESS_DENIED
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    zip_code = db.Column(db.String(10), nullable=False)
    categories = db.relationship('Category', secondary='user_cat', back_populates='users')


class Category(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy 
    cat_name = db.Column(db.String(100), unique=True, nullable=False)
    cat_des = db.Column(db.String(2000))
    question =  db.relationship('Question', backref='cat', lazy = True)
    users = db.relationship('User', secondary='user_cat', back_populates='categories')
    user_cat = db.relationship('UserCat', back_populates='category')

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True) # primary key for this table
    question_name = db.Column(db.String(1000), unique=True, nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)#foreign id of category table
    answer =  db.relationship('Answer', backref='quest', lazy = True)

class Answer(db.Model):
    ans_id = db.Column(db.Integer, primary_key=True) # primary key for this table
    content = db.Column(db.String(1000), unique=True, nullable=False)
    is_correct = db.Column(db.Boolean, unique=False, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable = False)#foreign id of category table

class UserCat(db.Model):
    __tablename__ = "user_cat"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    #this line is used for querying all the category that a user work on even they are duplicated
    category = db.relationship('Category', back_populates='user_cat')
    result = db.Column(db.Integer, nullable=False)