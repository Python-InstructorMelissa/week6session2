from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = 'week6_toDo'
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    @staticmethod
    def validate(user):
        isValid = True
        query = "SELECT * FROM users WHERE username = %(username)s;"
        altQuery = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query, user)
        eresults = connectToMySQL(User.db_name).query_db(altQuery, user)
        if len(results) >= 1:
            isValid = False
            flash("That username is already in the system!")
        if len(eresults) >= 1:
            isValid = False
            flash("That email is already regsistered!")
        if not EMAIL_REGEX.match(user['email']):
            isValid = False
            flash("Invalid email address")
        if len(user['password']) < 6:
            isValid = False
            flash("Password must be at least 6 characters long")
        if len(user['firstName']) < 2:
            isValid = False 
            flash("First name must be at least 2 characters long")
        if len(user['lastName']) < 2:
            isValid = False 
            flash("Last name must be at least 2 characters long")
        if len(user['username']) < 2:
            isValid = False 
            flash("Username must be at least 2 characters long")
        if user['password'] != user['confirm']:
            isValid = False
            flash("Your Passwords don't match")

        return isValid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (firstName, lastName, email, username, password) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(username)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getUsername(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod  
    def getEmail(cls, data):
        query =  "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])