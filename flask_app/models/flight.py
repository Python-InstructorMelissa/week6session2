from flask_app.config.mysqlconnection import connectToMySQL

class Flight:
    db = 'aircorp'
    def __init__(self, data):
        self.id = data['id']
        self.number = data['number']
        self.departing = data['departing']
        self.arriving = data['arriving']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.airline_id = data['airline_id']

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM flight;'
        results = connectToMySQL(cls.db).query_db(query)
        flights = []
        for row in results:
            flights.append(cls(row))
        return flights

    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM flight WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO flight (number, departing, arriving, airline_id) VALUES (%(number)s, %(departing)s, %(arriving)s, %(airline_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE flight SET number=%(number)s, departing=%(departing)s, arriving=%(arriving)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM flight WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)
