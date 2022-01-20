from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import squishy
    
class User:
    db = 'squishies'
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.squishies = []
    
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

    @classmethod
    def usersSquishy(cls, data):
        q = 'SELECT * FROM user LEFT JOIN squishy on squishy.user_id = user.id WHERE user.id = %(id)s;'
        r = connectToMySQL(cls.db).query_db(q, data)
        print("results: ", r)
        list = cls(r[0])
        for row in r:
            data = {
                'id': row['squishy.id'],
                'name': row['name'],
                'color': row['color'],
                'img': row['img'],
                'user_id': row['user_id']
            }
            s = squishy.Squishy(data)
            print("s: ", s)
            list.squishies.append(s)
        print('list: ', list)
        return list
