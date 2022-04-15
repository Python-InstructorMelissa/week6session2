from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.cohort import Cohort
from flask_app.models.subject import Subject
from flask_app.models.user import User

# Display all render template
@app.route('/cohorts/')
def cohorts():
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    theUser = User.getOne(userData)
    theCohorts = Cohort.getAll()
    theSubjects = Subject.getAll()
    return render_template('cohorts.html', cohorts=theCohorts, subjects=theSubjects, user=theUser)

# display form to create render template
@app.route('/cohorts/new/')
def newCohort():
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    theUser = User.getOne(userData)
    theSubjects = Subject.getAll()
    return render_template('newCohort.html', subjects=theSubjects, user=theUser)

# create redirect
@app.route('/cohorts/create/', methods=['post'])
def createCohort():
    data = {
        'name': request.form['name'],
        'instructor': request.form['instructor'],
        'cohortLength': request.form['cohortLength'],
        'subject_id': request.form['subject_id']
    }
    Cohort.save(data)
    print("saved the cohort: ", data)
    return redirect('/cohorts/')

# display one render template
@app.route('/cohorts/<int:cohort_id>/view/')
def viewCohort(cohort_id):
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    theUser = User.getOne(userData)
    data = {
        'id': cohort_id
    }
    theSubjects = Subject.getAll()
    return render_template('viewCohort.html', user=theUser, cohort=Cohort.getOne(data), subjects=theSubjects)

# edit one render template
@app.route('/cohorts/<int:cohort_id>/edit/')
def editCohort(cohort_id):
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    theUser = User.getOne(userData)
    data = {
        'id': cohort_id
    }
    theSubjects = Subject.getAll()
    return render_template('editCohort.html', user=theUser, cohort=Cohort.getOne(data), subjects=theSubjects)

# update one redirect
@app.route('/cohorts/<int:cohort_id>/update/', methods=['post'])
def updateCohort(cohort_id):
    data = {
        'id': cohort_id,
        'name': request.form['name'],
        'instructor': request.form['instructor'],
        'cohortLength': request.form['cohortLength'],
        'subject_id': request.form['subject_id']
    }
    Cohort.update(data)
    flash("You updated the cohort information")
    return redirect(f'/cohorts/{cohort_id}/view/')

# delete one redirect
@app.route('/cohorts/<int:cohort_id>/delete/')
def deleteCohort(cohort_id):
    data = {
        'id': cohort_id
    }
    Cohort.delete(data)
    flash("Cohort Deleted")
    return redirect('/cohorts/')