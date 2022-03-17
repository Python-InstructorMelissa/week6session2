from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.booking import Booking
from flask_app.models.user import User
from flask_app.models.flight import Flight

# Load form to book flight
@app.route('/flights/<int:flight_id>/book/')
def bookFlight(flight_id):
    data = {
        'id': session['user_id'],
    }
    flightData = {
        'id': flight_id
    }
    return render_template('bookFlight.html', user=User.getOne(data), flight=Flight.getOne(flightData))

@app.route('/saveBooking/', methods=['POST'])
def saveBooking():
    data = {
        'firstName': request.form['firstName'],
        'lastaName': request.form['lastaName'],
        'passengers': request.form['passengers'],
        'adultPassengers': request.form['adultPassengers'],
        'flightDate': request.form['flightDate'],
        'bagCheck': request.form['bagCheck'],
        'user_id': session['user_id'],
        'flight_id': request.form['flight_id'],
    }
    Booking.save(data)
    return redirect('/dashboard/')

@app.route('/booking/<int:booking_id>/edit/')
def editBooking(booking_id):
    pass

@app.route('/booking/<int:booking_id>/update/')
def updateBooking(booking_id):
    pass

@app.route('/booking/<int:booking_id>/delete/')
def deleteBooking(booking_id):
    pass