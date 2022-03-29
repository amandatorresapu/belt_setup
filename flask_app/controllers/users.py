from flask import Flask, render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.car import Car


@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("index.html")

@app.route("/clear_session")
def clear_session():
    session.clear()
    return redirect("/")

@app.route('/cars/edit/<int:id>')
def edit_car(id):
    if "user_id" not in session:
        return redirect("/dashboard")
    data = {"id": id}
    car = Car.get_one(data)
    return render_template('edit.html', car = car)

@app.route("/cars/edit/<int:id>", methods=["POST"])
def edit_the_car(id):        
    if not Car.car_validator(request.form):
        
        return redirect(f"/cars/edit/{id}")
    data = {
        "price": request.form["price"],
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "description": request.form["description"],
        "id": id,
    }
    Car.edit_car(data)
    return redirect('/dashboard')

@app.route("/users/create", methods = ["POST"]) 
def create_user():
    if User.registry_validator(request.form):
        session["user_id"] = User.create(request.form)
    return redirect("/dashboard")

@app.route("/login", methods = ["POST"])
def login():
    if not User.login_validator(request.form):
        flash("invalid login")
        return redirect("/")

    user = User.get_by_email(request.form)

    session["user_id"] = user.id
    print(session["user_id"])
    return redirect("/dashboard")