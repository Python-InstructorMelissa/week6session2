from app.config.mysqlconnection import connectToMySQL
from flask import flash

class Tasks:
    db_name = 'week6_toDo'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.info = data['info']
        self.user_id = data['user_id']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    @staticmethod
    def validate(task):
        isValid = True
        query = "SELECT * FROM tasks WHERE name = %(name)s;"
        results = connectToMySQL(cls.db_name).query_db(query, task)
        if len(results) >= 1:
            isValid = False
            flash("Sorry that task is already listed")
        if len(task['name']) < 4:
            isValid = False
            flash("Please use more than 4 characters for the task name")
        if len(task['info']) < 4:
            isValid = False
            flash("Please make sure to give a good description")

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM tasks;"
        results = connectToMySQL(cls.db_name).query_db(query)
        tasks = []
        for task in results:
            tasks.append(cls(task))
        return tasks

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM tasks WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO tasks (name, info, user_id) VALUES (%(name)s, %(info)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)