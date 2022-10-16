from unicodedata import name
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from project.auth import login
from . import db
from .models import Category, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
def home():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/admin')
@login_required
def admin():
    return render_template('admin.html', name=current_user.name)

#category management page
@main.route('/category')
@login_required
def category():
    #find all the categories in the system
    cats = Category.query.all()
    return render_template('category.html', name=current_user.name, cats = cats)

#call form create a new category
@main.route('/create')
@login_required
def create():
    return render_template('create_cat.html')

#create a new category
@main.route('/create', methods=['GET','POST'])
@login_required
def create_post():
    name = request.form.get('cat_name')
    des = request.form.get('cat_des')
    if not name:
        flash('Category name is required!!!')
    else:
        new_cat = Category(cat_name=name, cat_des=des)
        db.session.add(new_cat)
        db.session.commit()
        flash('Create Successful!!!')
    return render_template('create_cat.html')

#search category by name Like name%
@main.route('/search', methods=['POST'])
def search():
    catName = request.form['cat_name']
    print("Catname: ", catName)
    my_data = "%{}%".format(catName)
    cats = Category.query.filter(Category.cat_name.like(my_data)).all()
    return render_template('category.html', cats = cats)

#edit an existing category
@main.route('/<int:cat_id>/edit_cat', methods=('GET', 'POST'))
@login_required
def edit_cat(cat_id):
    cat = db.session.query(Category).filter(Category.id==cat_id).first()
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        cat_des = request.form['cat_des']

        if not cat_name:
            flash('Category name is required!')
        else:
            cat.cat_name = cat_name
            cat.cat_des = cat_des
            db.session.commit()
            flash('Congratulation! Update successful.')
            return render_template('edit_cat.html', cat=cat)

    return render_template('edit_cat.html', cat=cat)

#delete an existing category
@main.route('/<int:cat_id>/delete_cat', methods=('POST','GET'))
@login_required
def delete_cat(cat_id):
    cat = db.session.query(Category).filter(Category.id==cat_id).first()
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for('main.category'))

#----------------Manage user------------------
@main.route('/user')
@login_required
def user():
    #find all the categories in the system
    users = User.query.all()
    return render_template('user.html', users = users)
