from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.subject import Subject
from flask_app.models.user import User

# @app.route('/')
# def index():
#     return redirect('/subjects/')

@app.route('/subjects/')
def subjects():
    # knowing that I am going to display a table of all the subjects created on the html I call it subjects plural to remind myself multiple entries returned
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    print("all subjects from controller file: ", Subject.getAll())
    theUser = User.getOne(data)
    return render_template('subjects.html', subjects=Subject.getAll(), user=theUser)

@app.route('/subjects/new/')
def newSubject():
    # 26-32 added to keep non logged in users out
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    theUser = User.getOne(data)
    return render_template('newSubject.html', user=theUser)

@app.route('/subjects/create/', methods=['POST'])
def createSubject():
    data = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    Subject.save(data)
    print('Saved the Subject: ', data)
    return redirect('/subjects/')

@app.route('/subjects/<int:subject_id>/view/')
def viewSubject(subject_id):
    # lines 48-54 added to keep non logged in users out had to change 51 to userData to not confuse the function as to what data to user 
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    theUser = User.getOne(userData)
    data = {
        'id': subject_id
    }
    theClasses = Subject.getCohorts(data)
    print("controller get cohorts: ", theClasses)
    return render_template('viewSubject.html', subject=Subject.getOne(data), cohorts=theClasses, user=theUser)

@app.route('/subjects/<int:subject_id>/edit/')
def editSubject(subject_id):
    # lines 64-70 added to keep non logged in users out
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    theUser = User.getOne(userData)
    data = {
        'id': subject_id
    }
    return render_template('editSubject.html', subject=Subject.getOne(data), user=theUser)

@app.route('/subjects/<int:subject_id>/update/', methods=['post'])
def updateSubject(subject_id):
    data = {
        'id': subject_id,
        'name': request.form['name'],
        'description': request.form['description']
    }
    Subject.update(data)
    print("you have updated the subject:", data)
    return redirect(f'/subjects/{subject_id}/view/')

@app.route('/subjects/<int:subject_id>/delete/')
def deleteSubject(subject_id):
    data = {
        'id': subject_id
    }
    Subject.delete(data)
    return redirect('/subjects/')