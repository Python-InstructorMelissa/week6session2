from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.cohort import Cohort # This is needed for the join statement

class Subject:
    db = 'school'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.cohorts = []

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM subject;'
        results = connectToMySQL(cls.db).query_db(query)
        subjects = []
        for row in results:
            subjects.append(cls(row))
        return subjects

    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM subject WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO subject (name, description) VALUES (%(name)s, %(description)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE subject SET name=%(name)s, description=%(description)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM subject WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def getCohorts(cls, data):
        query = 'SELECT * FROM subject left join cohort on subject.id = cohort.subject_id where subject.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        print("the results in model: ", results)
        subject = cls(results[0])
        for row in results:
            cohortData = {
                'id': row['cohort.id'],
                'name': row['cohort.name'],
                'instructor': row['instructor'],
                'cohortLength': row['cohortLength'],
                'createdAt': row['cohort.createdAt'],
                'updatedAt': row['cohort.updatedAt'],
                'subject_id': row['subject_id']
            }
            print("the row in model: ", cohortData)
            subject.cohorts.append(Cohort(cohortData))
            print("after append in model: ", subject.cohorts)
        return subject.cohorts
