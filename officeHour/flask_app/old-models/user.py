from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
    
class User:
    db = 'lock_key'
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.userKey = data['userKey']
    
    @staticmethod
    def validate(u):
        isValid = True
        q = 'SELECT * FROM user WHERE username = %(username)s;'
        r = connectToMySQL(User.db).query_db(q, u)
        if len(r) >= 1:
            isValid = False
            flash("That username is already being used")
        if u['userKey'] != 'Squishies':
            isValid = False
            flash("That is the wrong Code")
        return isValid
    
    @classmethod
    def save(cls, data):
        q = 'INSERT INTO user (username, userKey) VALUES (%(username)s, %(userKey)s);'
        return connectToMySQL(cls.db).query_db(q, data)
    
    @classmethod
    def getAll(cls):
        q = 'SELECT * FROM user;'
        r = connectToMySQL(cls.db).query_db(q)
