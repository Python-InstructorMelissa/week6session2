from flask_app import app
from flask import Flask, render_template,  redirect, session, request, flash
from flask_app.models.airline import Airline
from flask_app.models import user

@app.route('/airlines/')
def airlines():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('airlines.html', airlines = Airline.getAll(), user=user.User.getOne(data))

@app.route('/airlines/add/')
def addAirline():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('addAirline.html', user=user.User.getOne(data))

@app.route('/airlines/create/', methods=['POST'])
def createAirline():
    data = {
        'name': request.form['name'],
        'headquarters': request.form['headquarters'],
        'locations': request.form['locations'],
        'workers': request.form['workers'],
        'planes': request.form['planes'],
    }
    Airline.save(data)
    return redirect('/airlines/')

@app.route('/airlines/<int:airline_id>/view/')
def viewAirline(airline_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    data = {
        'id': airline_id
    }
    flights = Airline.allFlights(data)
    print("all flights: ", flights)
    return render_template('viewAirline.html', airline=Airline.getOne(data), flights=Airline.allFlights(data), user=user.User.getOne(userData))

@app.route('/airlines/<int:airline_id>/edit/')
def editAirline(airline_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    data = {
        'id': airline_id
    }
    return render_template('editAirline.html', airline=Airline.getOne(data), user=user.User.getOne(userData))

@app.route('/airlines/<int:airline_id>/update/', methods=['POST'])
def updateAirline(airline_id):
    data = {
        'id': airline_id,
        'name': request.form['name'],
        'headquarters': request.form['headquarters'],
        'locations': request.form['locations'],
        'workers': request.form['workers'],
        'planes': request.form['planes'],
    }
    Airline.update(data)
    return redirect(f'/airlines/{airline_id}/view/')

@app.route('/airlines/<int:airline_id>/delete/')
def deleteAirline(airline_id):
    data = {
        'id': airline_id,
    }
    Airline.delete(data)
    return redirect('/airlines/')