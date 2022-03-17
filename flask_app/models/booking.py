from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import flight

class Booking:
    db = 'aircorp'
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastaName = data['lastaName']
        self.passengers = data['passengers']
        self.adultPassengers = data['adultPassengers']
        self.flightDate = data['flightDate']
        self.bagCheck = data['bagCheck']
        self.user_id = data['user_id']
        self.flight_id = data['flight_id']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM booking;'
        results = connectToMySQL(cls.db).query_db(query)
        bookings = []
        for row in results:
            bookings.append(cls(row))
        return bookings

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM booking WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO booking (firstName, lastaName, passengers, adultPassengers, flightDate, bagCheck, user_id, flight_id) VALUES (%(firstName)s, %(lastaName)s, %(passengers)s, %(adultPassengers)s, %(flightDate)s, %(bagCheck)s, %(user_id)s, %(flight_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE booking SET firstName=%(firstName)s, lastaName=%(lastaName)s, passengers=%(passengers)s, adultPassengers=%(adultPassengers)s, flightDate=%(flightDate)s, bagCheck=%(bagCheck)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM booking WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)
