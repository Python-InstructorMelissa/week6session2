from flask_app import app
from flask import Flask, render_template,  redirect, session, request, flash
from flask_app.models.flight import Flight
from flask_app.models.airline import Airline
from flask_app.models import user

@app.route('/flights/')
def flights():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('flights.html', flights=Flight.getAll(), airlines=Airline.getAll(), user=user.User.getOne(data))

@app.route('/flights/add/')
def addFlight():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('addFlight.html', airlines=Airline.getAll(), user=user.User.getOne(data))

@app.route('/flights/create/', methods=['POST'])
def createFlight():
    data = {
        'number': request.form['number'],
        'departing': request.form['departing'],
        'arriving': request.form['arriving'],
        'airline_id': request.form['airline_id'],
    }
    Flight.save(data)
    return redirect('/flights/')

@app.route('/flights/<int:flight_id>/view/')
def viewFlight(flight_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    data = {
        'id': flight_id
    }
    return render_template('viewFlight.html', flight=Flight.getOne(data), airlines=Airline.getAll(), user=user.User.getOne(userData))

@app.route('/flights/<int:flight_id>/edit/')
def editFlight(flight_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    data = {
        'id': flight_id
    }
    return render_template('editFlight.html', flight=Flight.getOne(data), airlines=Airline.getAll(), user=user.User.getOne(userData))

@app.route('/flights/<int:flight_id>/update/', methods=['POST'])
def updateFlight(flight_id):
    data = {
        'id': flight_id,
        'number': request.form['number'],
        'departing': request.form['departing'],
        'arriving': request.form['arriving'],
    }
    Flight.update(data)
    return redirect(f'/flights/{flight_id}/view/')

@app.route('/flights/<int:flight_id>/delete/')
def deleteFlight(flight_id):
    data = {
        'id': flight_id,
    }
    Flight.delete(data)
    return redirect('/flights/')