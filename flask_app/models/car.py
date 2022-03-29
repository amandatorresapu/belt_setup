from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import session, flash, redirect

class Car:
    def __init__(self, data):
        self.user_id = data["user_id"]
        self.id = data["id"]
        self.price = data["price"]
        self.model = data["model"]
        self.make = data["make"]
        self.year = data["year"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod 
    def create(cls,data):
        mysql = connectToMySQL("red_belt_db")
        query = "INSERT INTO cars (user_id, price, model, make, year, description) Values (%(user_id)s, %(price)s, %(model)s, %(make)s, %(year)s, %(description)s);"
        user_id = mysql.query_db(query, data)

        return user_id
        
    @classmethod 
    def car_get_all(cls):
        mysql = connectToMySQL("red_belt_db")
        query = "SELECT * FROM cars JOIN users on cars.user_id = users.id;"
        results = mysql.query_db(query)
        if results:
            cars = []
            for row in results:
                temp_car = cls(row)
                data = {
                    "id": row["users.id"],
                    "first_name" : row["first_name"],
                    "last_name" : row["last_name"],
                    "email" : row["email"],
                    "password" : row["password"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"]
                    }
                temp_car.user = user.User(data)
                cars.append(temp_car)
            return cars

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM cars WHERE cars.id = %(id)s;"
        results = connectToMySQL("red_belt_db").query_db(query, data)
        if results: 
            return cls(results[0])


    @classmethod
    def edit_car(cls,data):
        query = "UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s WHERE id = %(id)s;"
        connectToMySQL("red_belt_db").query_db(query, data)

    @classmethod
    def delete_car(cls, data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        connectToMySQL("red_belt_db").query_db(query, data)
    

    @staticmethod
    def car_validator(data):
        is_valid = True

        if (data["price"]) == "":
            price = 0
        else: price = int(data["price"])

        if (data["year"]) == "":
            year = 0
        else: year = int(data["year"])

        if (price) <= 1:
            flash("price must be more than 1")
            is_valid = False

        if len(data["model"]) <= 4:
            flash("Model must be more than 4 charaters in length")
            is_valid = False

        if len(data["make"]) <= 3:
            flash("Make must be more than 3 charaters in length")
            is_valid = False
        
        if (year) <= 1:
            flash("year must be greater than 0")
            is_valid = False

        if len(data["description"]) <= 1:
            flash("description must be more than 1")
            is_valid = False
        return is_valid
