from app import app
from flask import Flask, render_template, redirect, session, request
from  flask_bcrypt import Bcrypt
from app.models.user import User

bcrypt = Bcrypt(app)

# Main landing page - contains log/reg
@app.route('/')
def index():
    return render_template('index.html')

# Register route
@app.route('/register', methods=['POST'])
def register():
    isValid = User.validate(request.form)
    if not isValid:
        return redirect('/')
    newUser = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'username': request.form['username'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(newUser)
    if not id:
        flash("Something went wrong!")
        return redirect('/')
    session['user_id'] = id
    return redirect('/dashboard')

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = {
        'username': request.form['username']
    }
    user = User.getUsername(data)
    if not user:
        flash("Invalid Login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Wrong password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

# Logout function
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')