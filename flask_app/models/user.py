from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import booking
from flask_app.models import flight
from flask_app.models import airline
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
        self.booking = None
        self.flight = None
        self.airline = None
        self.flights = []
    
    def fullName(self):
        return f'{self.firstName} {self.lastName}'

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
    def updateEmployee(cls, data):
        query = 'UPDATE user SET access=9 WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        pass

    @classmethod
    def userBookings(cls, data):
        query = 'SELECT * FROM user Left JOIN booking ON user.id = booking.user_id LEFT JOIN flight ON booking.flight_id = flight.id LEFT JOIN airline ON flight.airline_id = airline.id WHERE user.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        print('userBookings model results: ', results)
        user = cls(results[0])
        for row in results:
            bookingData = {
                'id': row['booking.id'],
                'firstName': row['booking.firstName'],
                'lastaName': row['lastaName'],
                'passengers': row['passengers'],
                'adultPassengers': row['adultPassengers'],
                'flightDate': row['flightDate'],
                'bagCheck': row['bagCheck'],
                'createdAt': row['booking.createdAt'],
                'updatedAt': row['booking.updatedAt'],
                'user_id': row['user_id'],
                'flight_id': row['flight_id'],
            }
            oneBooking = booking.Booking(bookingData)
            user.booking = oneBooking
            # Created a field for each  for this it is booking and set to none
            flightData = {
                'id': row['flight.id'],
                'number': row['number'],
                'departing': row['departing'],
                'arriving': row['arriving'],
                'createdAt': row['flight.createdAt'],
                'updatedAt': row['flight.updatedAt'],
                'airline_id': row['airline_id'],
            }
            oneFlight = flight.Flight(flightData)
            user.flight = oneFlight
            airlineData = {
                'id': row['airline.id'],
                'name': row['name'],
                'headquarters': row['headquarters'],
                'locations': row['locations'],
                'workers': row['workers'],
                'planes': row['planes'],
                'createdAt': row['airline.createdAt'],
                'updatedAt': row['airline.updatedAt'],
            }
            oneAirline = airline.Airline(airlineData)
            user.airline = oneAirline
            # here we are taking these new single use values that were none and appending them to the flights then since it is single use or just a string that keeps getting updated each loop it will have new data and thus append new info...
            user.flights.append(user)
            print('each row of users flights userBooking Model: ', bookingData, flightData, airlineData)
        print("printing list after append in model: ", user.flights)
        return user.flights