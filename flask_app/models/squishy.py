from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Squishy:
    db = 'squishies'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.color = data['color']
        self.img = data['img']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        q = 'INSERT INTO squishy (name, color, img, user_id) VALUES (%(name)s, %(color)s, %(img)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def getAll(cls):
        q = 'SELECT * FROM squishy;'
        r = connectToMySQL(cls.db).query_db(q)
        squishies = []
        for s in r:
            squishies.append(cls(s))
        return squishies

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM squishy WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def delete(cls, data):
        q = "DELETE FROM squishy WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE squishy SET name=%(name)s, color=%(color)s, img=%(img)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)
