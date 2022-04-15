from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/', methods=['post'])
def register():
    isValid = User.validate(request.form)
    if not isValid: # if isValid = False the redirect as this statement will run
        return redirect('/')
    newUser = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(newUser)
    if not id:
        flash('Something got messed up somewhere')
        return redirect('/')
    session['user_id'] = id
    flash("You are now logged in")
    return redirect('/dashboard/')

@app.route('/login/', methods=['post'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.getEmail(data) # Checking to see if the email is in our system
    if not user: # if it isn't please run this part of the code
        flash("Yoo man thats not in our system!")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Forgot your password again didn't you?")
        return redirect('/')
    session['user_id'] = user.id
    flash("You are now logged in")
    return redirect('/dashboard/')

@app.route('/logout/')
def logout():
    session.clear()
    flash("You have now been logged out")
    return redirect('/')

@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    theUser = User.getOne(userData)
    if theUser.id == 1:
        if theUser.access == 9:
            return redirect('/subjects/')
        else:
            User.makeTeacher(userData)
            flash('User access updated you are now a teacher')
            return redirect('/subjects/')
    if theUser.access == 9:
        return redirect('/subjects/')
    else:
        allClasses = User.userClasses(userData)
        return render_template('dashboard.html', user=theUser, classes=allClasses)
