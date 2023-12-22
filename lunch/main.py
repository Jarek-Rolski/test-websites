from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import os
from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import argparse

app = Flask(__name__)

def simple(env, resp):
    resp(b'200 OK', [(b'Content-Type', b'text/plain')])
    return [b'Hello WSGI World']

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

from database_management import list_restaurants, list_reviews, list_rating
from database_management import add_restaurant, add_review, save_rating

class Restaurant(FlaskForm):
    name = StringField('Restaurant name', validators=[DataRequired()])
    location = StringField('Location on Google Maps', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')

class RestaurantReview(FlaskForm):
    restaurants = list_restaurants()
    restaurants_names = [restautrant['Name'] for restautrant in restaurants]
    name = SelectField('Restaurant name', choices=restaurants_names, validators=[DataRequired()])
    text = StringField('Review', validators=[])
    quality = SelectField('Food quality', choices=["😋", "😋😋", "😋😋😋", "😋😋😋😋", "😋😋😋😋😋"],
                           validators=[DataRequired()])
    quantity = SelectField('Food quantity', choices=["🍕", "🍕🍕", "🍕🍕🍕", "🍕🍕🍕🍕", "🍕🍕🍕🍕🍕"],
                            validators=[DataRequired()])
    price = SelectField('food price', choices=["💲", "💲💲", "💲💲💲", "💲💲💲💲", "💲💲💲💲💲"],
                             validators=[DataRequired()])
    overall = SelectField('Overall experience', choices=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
                             validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/add-restaurant', methods=['GET', 'POST'])
def add_restaurant_web():
    form = Restaurant()
    if form.validate_on_submit():
        print("True")
        name = form.name.data
        location = form.location.data
        add_restaurant(name, location)
        return redirect(url_for("restaurants"))

    return render_template('add_restaurant.html', form=form)

@app.route('/add-review', methods=['GET', 'POST'])
def add_review_web():
    form = RestaurantReview()
    restaurants = list_restaurants()
    restaurants_names = [restautrant['Name'] for restautrant in restaurants]
    form.name.choices = restaurants_names
    if form.validate_on_submit():
        print("True")
        name = form.name.data
        text = form.text.data
        quality = form.quality.data
        quality = len(quality.split("😋"))-1
        quantity = form.quantity.data
        quantity = len(quantity.split("🍕"))-1
        price = form.price.data
        price = len(price.split("💲"))-1
        overall = form.overall.data
        overall = len(overall.split("⭐"))-1
        add_review(name,text,quality,quantity,price,overall)
        save_rating()
        return redirect(url_for("reviews"))

    return render_template('add_review.html', form=form)

@app.route('/restaurants')
def restaurants():
    restaurants = list_restaurants()
    ratings = list_rating()
    for restaurant in restaurants:
        restaurant['quality'] = "-"
        restaurant['quantity'] = "-"
        restaurant['price'] = "-"
        restaurant['overall'] = "-"
        for rating in ratings:
            if rating['Name']==restaurant['Name']:
                restaurant['quality'] = int(round(rating['quality'],0))*"😋"
                restaurant['quantity'] = int(round(rating['quantity'],0))*"🍕"
                restaurant['price'] = int(round(rating['price'],0))*"💲"
                restaurant['overall'] = int(round(rating['overall'],0))*"⭐"
                break
    list_of_rows = [["Name", "Location", "Quality", "Quantity", "Price", "Overall"]] + [list(r.values()) for r in restaurants]
    return render_template('restaurants.html', cafes=list_of_rows)

@app.route('/reviews')
def reviews():
    reviews = list_reviews()
    for review in reviews:
        review['quality'] = int(round(review['quality'],0))*"😋"
        review['quantity'] = int(round(review['quantity'],0))*"🍕"
        review['price'] = int(round(review['price'],0))*"💲"
        review['overall'] = int(round(review['overall'],0))*"⭐"

    list_of_rows = [["Name", "Review", "Quality", "Quantity", "Price", "Overall"]] + [list(r.values()) for r in reviews]
    return render_template('reviews.html', cafes=list_of_rows)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--root_path', default='', type=str, help='Root path')
    args = parser.parse_args()

    PREFIX = args.root_path

    app.config['APPLICATION_ROOT'] = PREFIX

    app.wsgi_app = DispatcherMiddleware(simple, {PREFIX: app.wsgi_app})

    app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
    Bootstrap(app)

    app.run(debug=True, host='0.0.0.0', port=8080)
