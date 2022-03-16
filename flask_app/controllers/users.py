from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/', methods=['POST'])
def register():
    isValid = User.validate(request.form)
    if not isValid:  # if isValid = False then redirect to /
        return redirect('/')
    newUser = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(newUser)
    if not id:
        flash('Something went wrong')
        return redirect('/')
    session['user_id'] = id
    flash("You are now logged in")
    return redirect('/airlines/')

@app.route('/login/', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.getEmail(data) # check if the email is in the database
    if not user: # if not let them know
        flash('That email is not in our database please register')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Wrong password')
        return redirect('/')
    session['user_id'] = user.id
    flash("You are now logged in")
    return redirect('/airlines/')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=user.User.getOne(data))