from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import subject

class Cohort:
    db = 'school'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.instructor = data['instructor']
        self.cohortLength = data['cohortLength']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.subject_id = data['subject_id']

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM cohort;'
        results = connectToMySQL(cls.db).query_db(query)
        cohorts = []
        for row in results:
            cohorts.append(cls(row))
        return cohorts

    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM cohort WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO cohort (name, instructor, cohortLength, subject_id) VALUES (%(name)s, %(instructor)s, %(cohortLength)s, %(subject_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE cohort SET name=%(name)s, instructor=%(instructor)s, cohortLength=%(cohortLength)s, subject_id=%(subject_id)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM cohort WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)