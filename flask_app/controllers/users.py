from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.airline import Airline
from flask_app.models.flight import Flight
from flask_app.models.booking import Booking

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
    return redirect('/dashboard/')

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
    return redirect('/dashboard/')

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
    # Creating code to make certain users an employee upon reaching this page
    theUser = User.getOne(data)
    if theUser.id == 1:
        if theUser.access == 9:
            return redirect('/airlines/')
        else:
            User.updateEmployee(data)
            flash('User access updated to Employee level 9')
            return redirect('/airlines/')
    else:
        bookings = User.userBookings(data)
        print("************ all booking from controller: ", bookings)
        return render_template('dashboard.html', user=User.getOne(data), bookings = User.userBookings(data))

@app.route('/users/')
def users():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.getOne(data)
    if user.access == 9:
        return render_template('users.html', user=User.getOne(data), allUsers=User.getAll())
    else:
        flash('You are not authorized to view this page')
        return redirect('/dashboard/')

@app.route('/users/<int:user_id>/createEmployee/')
def createEmployee(user_id):
    data = {
        'id': user_id
    }
    User.updateEmployee(data)
    flash('User updated to employee')
    return redirect('/users/')