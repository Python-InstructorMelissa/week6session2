from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db_name = 'mock_store'
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.username = data['username']
        self.password = data['password']
        self.createAt = data['createAt']
        self.updatedAt = data['updatedAt']

    @staticmethod
    def validate(user):
        isValid = True
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(results) >= 1:
            isValid = False
            flash("That username is already in the system!")
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
        query = "INSERT INTO users (firstName, lastName, username, password) VALUES (%(firstName)s, %(lastName)s, %(username)s, %(password)s);"
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
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)