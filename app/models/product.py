from app.config.mysqlconnection import connectToMySQL
from flask import flash

class Product:
    db_name = 'mock_store'
    def __init__(self, data):
        self.id = data['id']
        self.pName = data['pName']
        self.pDesc = data['pDesc']
        self.pPrice = data['pPrice']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO products (pName, pDesc, pPrice, users_id) VALUES (%(pName)s, %(pDesc)s, %(pPrice)s, %(users_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM products;"
        results = connectToMySQL(cls.db_name).query_db(query)
        products = []
        for product in results:
            products.append(cls(product))
        return products