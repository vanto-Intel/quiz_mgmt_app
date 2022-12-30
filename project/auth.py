#from msilib.schema import AdminExecuteSequence
import re
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db
from .send_zip import SendZipClient
from sqlalchemy.orm import scoped_session

from .models import Category, User, Question, UserCat

#print ('city name: %s and temperature: %s' %(city, temperature))

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')
    
@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    zipcode = request.form.get('zipcode')
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), zip_code=zipcode)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    #get city name and temperature based on the user's zipcode
    city = 'Portland'
    temperature = '45'
    
    # try:
    #     rpc = SendZipClient(user.zip_code)
    #     response = rpc.call()
    #     city = response['name']
    #     temperature = response['main']['temp']
    # except Exception as re:
    #     print(re)

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    categories = Category.query.join(UserCat).join(User).filter(User.id==user.id).all()

    # access the results for each category
    # for category in categories:
    #     for user_cat in category.user_cat:
    #         if user_cat.user_id == user.id:
    #             result = user_cat.result
    #             print(f'Category: {category.cat_name}, Result: {result}')

    #session here
    session['user_id'] = user.id 
    login_user(user, remember=remember)
    if user.name == 'admin':
        return redirect(url_for('main.admin', city=city, temp=temperature))
    return redirect(url_for('main.member', city=city, temp=temperature))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))