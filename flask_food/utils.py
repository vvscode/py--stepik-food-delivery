import csv
from collections import namedtuple

import click
from flask import session
from sqlalchemy.exc import IntegrityError

from flask_food.extensions import db
from flask_food.models import Category, Meal

Cart = namedtuple("Cart", ["items", "meals", "amount"])


def create_categories(name):
    category = Category(title=name)
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    else:
        click.echo(f"Added Category {name.capitalize()}")


def create_meals(meal_data):
    category = Category.query.filter(
        Category.title == meal_data.get("category"),
    ).first()
    meal_image = meal_data.get("picture")
    meal = Meal(
        title=meal_data.get("title"),
        description=meal_data.get("description"),
        picture=f"images/{meal_image}",
        price=meal_data.get("price"),
        category=category,
    )
    db.session.add(meal)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    else:
        click.echo(f"Aded meal {meal.title} from category {meal.category}")


def fill_db(meal_csv="data/menu.csv"):
    meals = []
    with open(meal_csv) as csv_fiile:
        meals_data = csv.DictReader(csv_fiile, delimiter=",")
        for meal in meals_data:
            meals.append(meal)

    categories = {meal["category"] for meal in meals}
    for category in categories:
        create_categories(category)
    for meal_data in meals:
        create_meals(meal_data)


def check_cart():
    if not session.get("cart"):
        return Cart([], [], 0)
    cart_items = set(session.get("cart"))
    cart_meals = Meal.query.filter(Meal.id.in_(cart_items)).all()
    cart_amount = sum(meal.price for meal in cart_meals)
    return Cart(cart_items, cart_meals, cart_amount)


if __name__ == "__main__":
    fill_db()
