from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.car import Car
from flask_app.models.user import User

@app.route('/new_car')
def new_car():
    return render_template('new_car.html')

@app.route('/show/<int:id>')
def show(id):
    data = {
        "id": id
    }
    
    car = Car.get_one(data)
    return render_template('show.html', car = car)



@app.route("/dashboard")
def all_cars_all_users():
    if "user_id" not in session:
        return redirect("/")
    user=User.get_one({"id": session["user_id"]})
    all_cars = Car.car_get_all()
    return render_template("dashboard.html", all_cars = all_cars, user=user)

@app.route("/car/<int:id>/delete")
def delete(id):
    data = {
    "id": id
    }
    print(data)
    Car.delete_car(data) 
    return redirect('/dashboard')




@app.route('/car/create', methods = ["POST"])
def create():
    if Car.car_validator(request.form):
        flash("invalid information")
        return redirect("/new_car")
    Car.create(request.form)
    return redirect('/new_car')


