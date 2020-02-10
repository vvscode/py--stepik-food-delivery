from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy_utils import ChoiceType, EmailType, PhoneNumber
from werkzeug.security import check_password_hash, generate_password_hash

from flask_food.extensions import db, login

orders_meals = db.Table(
    "orders_meals",
    db.Column("meal_id", db.Integer, db.ForeignKey("meal.id"), primary_key=True),
    db.Column("order_id", db.Integer, db.ForeignKey("order.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def validate_password(self, password):
        return check_password_hash(self.password, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    meals = db.relationship("Meal", back_populates="category", lazy="joined")


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400))
    picture = db.Column(db.String(100))
    price = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category", back_populates="meals", lazy="joined")
    orders = db.relationship(
        "Order", secondary="orders_meals", back_populates="meals", lazy="joined",
    )


class Order(db.Model):
    STATUS_TYPES = [
        ("NEW", "Новый"),
        ("DELIVERING", "Выполняется"),
        ("DONE", "Готово"),
    ]
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    amount = db.Column(db.Integer)
    status = db.Column(ChoiceType(STATUS_TYPES), default="NEW")
    client_name = db.Column(db.String(25), nullable=False)
    client_address = db.Column(db.String(250), nullable=False)
    client_email = db.Column(EmailType, nullable=False)
    client_phone = db.Column(db.String)
    meals = db.relationship(
        "Meal", secondary="orders_meals", back_populates="orders", lazy="joined",
    )


@event.listens_for(User.password, "set", retval=True)
def hash_user_password(target, value, *args):  # noqa:WPS110
    return generate_password_hash(value)


@event.listens_for(Order.client_phone, "set", retval=True)
def format_phone(turget, number, *args):
    return PhoneNumber(number, region="RU").international


@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))
