from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import booking
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'aircorp'
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.access = data['access']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    @staticmethod
    def validate(user):
        isValid = True
        query = 'SELECT * FROM user WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            isValid = False
            flash("That email is already in our database")
        if not EMAIL_REGEX.match(user['email']):
            isValid = False
            flash("Invalid email format")
        if len(user['firstName']) < 2:
            isValid = False
            flash('Please use at least 2 characters for the first name')
        if len(user['lastName']) < 2:
            isValid = False
            flash('Please use at least 2 characters for the last name')
        if len(user['password']) < 8:
            isValid = False
            flash('Password must be at least 8 characters long')
        if user['password'] != user['confirm']:
            isValid = False
            flash('Passwords do not match')
        return isValid

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM user;'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getEmail(cls, data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO user (firstName, lastName, email, password) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        pass

    @classmethod
    def userBookings(cls, data):
        # 1 user all their booking using a left join
        pass