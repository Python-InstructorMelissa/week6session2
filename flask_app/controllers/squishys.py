import re
from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.squishy import Squishy
from flask_app.models.user import User


@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        user = User.getOne(data)
        squishy = Squishy.getAll()
        print("Session User: ", user)
        return render_template('dashboard.html', user=user, squishy=squishy)

@app.route('/addSquishy/')
def addSquishy():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        user = User.getOne(data)
        return render_template('addSquishy.html', user=user)

@app.route('/createSquishy/', methods=['POST'])
def createSquishy():
    data = {
        'name': request.form['name'],
        'color': request.form['color'],
        'img': request.form['img'],
        'user_id': request.form['user_id']
    }
    Squishy.save(data)
    return redirect('/dashboard/')

@app.route('/squishy/<int:squishy_id>/view/')
def viewSquishy(squishy_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        user = User.getOne(data)
        data1 = {
            'id': squishy_id
        }
        squishy = Squishy.getOne(data1)
        return render_template('viewSquishy.html', user=user, squishy=squishy)

@app.route('/squishy/<int:squishy_id>/delete/')
def deleteSquishy(squishy_id):
    data = {
        'id': squishy_id
    }
    Squishy.delete(data)
    return redirect('/dashboard/')
    
@app.route('/squishy/<int:squishy_id>/edit/')
def editSquishy(squishy_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        user = User.getOne(data)
        data1 = {
            'id': squishy_id
        }
        squishy = Squishy.getOne(data1)
        return render_template('editSquishy.html', user=user, squishy=squishy)


@app.route('/squishy/<int:squishy_id>/update/', methods=['POST'])
def updateSquishy(squishy_id):
    data = {
        'id': squishy_id,
        'name': request.form['name'],
        'color': request.form['color'],
        'img': request.form['img'] 
    }
    Squishy.update(data)
    return redirect('/dashboard/')