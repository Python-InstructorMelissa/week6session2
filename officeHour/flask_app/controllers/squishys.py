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
        users = User.getAll()
        user = User.getOne(data)
        print("all Users: ", users)
        print("Session User: ", user)
        return render_template('dashboard.html', users=users, user=user)