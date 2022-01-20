from app.config.mysqlconnection import connectToMySQL
from flask import flash

class Squishy:
    db = 'lock_key'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.color = data['color']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        q = 'INSERT INTO squishy (name, color, user_id) VALUES (%(name)s, %(color)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def getAll(cls):
        q = 'SELECT * FROM squishy;'
        r = connectToMySQL(cls.db).query_db(q)
        squishies = []
        for s in r:
            squishies.append(cls(s))
