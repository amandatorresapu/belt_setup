import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import car
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)   


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls,data):
        hash_yellow = bcrypt.generate_password_hash(data['password'])
        hashed_dict = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "password": hash_yellow
        }
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("red_belt_db").query_db(query,hashed_dict)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("red_belt_db").query_db(query, data)
        if result: 
            return cls(result[0])

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("red_belt_db").query_db(query, data)
        if results: 
            return cls(results[0])

    @staticmethod
    def login_validator(data):
        user = User.get_by_email(data)
        if not user:
            return False
        
        if not bcrypt.check_password_hash(user.password, data["password"]):
            return False

        return True

    @staticmethod
    def registry_validator(data):
        is_valid = True
        
        if len(data["first_name"]) <= 2:
            flash("username must be at least 3 characters!!")
            is_valid = False
            
        user = User.get_by_email(data)
        if len(data["last_name"]) <= 2:
            flash("username must be at least 3 characters!!")
            is_valid = False

        if user:
            flash("email already in use")
            is_valid = False

        EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email")
            is_valid = False

        if len(data["email"]) <= 3:
            flash("Emails must be at least 4 characters long!")

        if len(data["password"]) <= 8:
            flash("Password must be 8 charaters or more")
            is_valid = False

        if data["password"] != data["confirm_password"]:
            flash("Password and confirm must match")
            is_valid = False

        return is_valid


    
