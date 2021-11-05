from app import app
from flask import Flask, render_template, redirect, session, request, flash
import re
from  flask_bcrypt import Bcrypt
from app.models.user import User
from app.models.product import Product


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.getOne(data), items=Product.getAll(), getItems=Product.getItemsUsername())

@app.route('/product/createProd', methods=['POST'])
def createProd():
    data = {
        'pName': request.form['pName'],
        'pDesc': request.form['pDesc'],
        'pPrice': request.form['pPrice'],
        'users_id': request.form['users_id']
    }
    Product.save(data)
    return redirect('/dashboard')