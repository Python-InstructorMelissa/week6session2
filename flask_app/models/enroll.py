from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import cohort


class Enroll:
    db = 'school'
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.startDate = data['startDate']
        self.selfPace = data['selfPace']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.cohort_id = data['cohort_id']

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM enroll;'
        results = connectToMySQL(cls.db).query_db(query)
        enrolls = []
        for row in results:
            enrolls.append(cls(row))
        return enrolls

    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM enroll WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO enroll (firstName, lastName, email, startDate, selfPace, user_id, cohort_id) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(startDate)s, %(selfPace)s, %(user_id)s, %(cohort_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE enroll SET firstName=%(firstName)s, lastName=%(lastName)s, email=%(email)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM enroll WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)