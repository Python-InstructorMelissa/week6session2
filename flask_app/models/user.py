from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import cohort
from flask_app.models import subject
from flask_app.models import enroll
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'school'
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.access = data['access']
        self.createdAt = data['createdAt']
        self.updatedAT = data['updatedAT']
        self.enrolled = None
        self.subject = None
        self.cohort = None
    
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
    def makeTeacher(cls, data):
        query = 'UPDATE user SET access=9 WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        pass

    @classmethod
    def userClasses(cls, data):
        query = "SELECT * FROM user left join enroll on user.id = enroll.user_id left join cohort on enroll.cohort_id = cohort.id left join subject on cohort.subject_id = subject.id WHERE user.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        allClasses = []
        for row in results:
            user = cls(row)
            enrollData = {
                'id': row['enroll.id'],
                'firstName': row['enroll.firstName'],
                'lastName': row['enroll.lastName'],
                'email': row['enroll.email'],
                'startDate': row['startDate'],
                'selfPace': row['selfPace'],
                'createdAt': row['enroll.createdAt'],
                'updatedAt': row['updatedAt'],
                'user_id': row['user_id'],
                'cohort_id': row['cohort_id'],
            }
            oneEnroll = enroll.Enroll(enrollData)
            user.enrolled = oneEnroll
            cohortData = {
                'id': row['cohort.id'],
                'name': row['name'],
                'instructor': row['instructor'],
                'cohortLength': row['cohortLength'],
                'createdAt': row['cohort.createdAt'],
                'updatedAt': row['cohort.updatedAt'],
                'subject_id': row['subject_id'],
            }
            user.cohort = cohort.Cohort(cohortData)
            subjectData = {
                'id': row['subject.id'],
                'name': row['subject.name'],
                'description': row['description'],
                'createdAt': row['subject.createdAt'],
                'updatedAt': row['subject.updatedAt'],
            }
            user.subject = subject.Subject(subjectData)
            allClasses.append(user)
        return allClasses

    def fullName(self):
        return f'{self.firstName} {self.lastName}'