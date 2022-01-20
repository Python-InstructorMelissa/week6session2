from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
    
class User:
    db = 'squishies'
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
    
    @staticmethod
    def validate(u):
        isValid = True
        q = 'SELECT * FROM user WHERE username = %(username)s;'
        r = connectToMySQL(User.db).query_db(q, u)
        if len(r) >= 1:
            isValid = False
            flash("That username is already being used")
        if u['password'] != u['confirm']:
            isValid = False
            flash("Your Passwords don't match")
        return isValid
    
    @classmethod
    def save(cls, data):
        q = 'INSERT INTO user (username, password) VALUES (%(username)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    @classmethod
    def getAll(cls):
        q = 'SELECT * FROM user;'
        r = connectToMySQL(cls.db).query_db(q)
        users = []
        for user in r:
            users.append(cls(user))
        return users

    @classmethod
    def getUsername(cls, data):
        query = "SELECT * FROM user WHERE username = %(username)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
