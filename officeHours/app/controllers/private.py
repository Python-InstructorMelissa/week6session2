from app import app
from flask import Flask, render_template, redirect, session, request, flash
import re
from  flask_bcrypt import Bcrypt
from app.models.user import User
from app.models.toDo import Tasks




@app.route('/toDoApp')
def toDo():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('toDo.html', user=User.getOne(data), tasks=Tasks.getAll())

@app.route('/createTask', methods=['POST'])
def createTask():
    data = {
        'name': request.form['name'],
        'info': request.form['info'],
        'user_id': request.form['user_id']
    }
    Tasks.save(data)
    return redirect('/toDoApp')