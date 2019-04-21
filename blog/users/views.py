from flask import Blueprint, url_for, redirect, render_template, request, flash
from blog import db, login_manager
from blog.models import User, load_user
from blog.users.forms import LoginForm, AccountInfoForm
from flask_login import login_user, login_required, logout_user, current_user

users_blueprint = Blueprint('users',__name__, template_folder='templates/')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': 
        email = request.form['email']
        password = request.form['password']

        new_user = User(email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit() 

        return redirect(url_for('users.login'))

    return render_template('users/register.html')

@users_blueprint.route('/list')
@login_required
def list():
    users = User.query.all()
    return render_template('users/list.html', users=users)

@users_blueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountInfoForm()
    favorites=current_user.favorite

    if request.method == 'GET': 
        form.username.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit(): 
        username = form.username.data
        email = form.email.data

        current_user.username = username
        current_user.email = email 

        db.session.commit()
        flash('User account updated', 'success')
        
        return redirect(url_for('users.account'))
        
    return render_template('users/account.html',
                                     form=form, 
                                     favorites=favorites)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    email = form.email.data
    password = form.password.data

    if form.validate_on_submit(): 

        user = User.query.filter_by(email=email).first()

        if user is not None and user.check_password(password):
            
            login_user(user) 
            flash('You have successfully log in', 'success')
            next = request.args.get('next')

            return redirect(url_for('users.account') or next)
        
        else: 
            
            flash('Wrong combination of email/password', 'danger')
            return redirect(url_for('users.login'))
            
    return render_template('users/login.html', form=form)

@users_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have successfully logged out', 'success')
    return redirect(url_for('users.login'))