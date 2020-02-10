from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.fields.j25 import EmailField, TelField
from wtforms.validators import Email, EqualTo, Length, Regexp

from flask_food.validators import validate_phone, password_validators


class OrderForm(FlaskForm):
    name = StringField(label="Ваше имя")
    address = StringField(label="Адрес")
    email = EmailField(
        label="Электропочта", validators=[Email(message="Неверный адрес почты.")],
    )
    phone = TelField("Телефон", validators=[validate_phone])


class LoginForm(FlaskForm):
    email = EmailField(label="", validators=[Email(message="Неверный адрес почты.")])
    password = PasswordField(label="")
    remembered = BooleanField(label="Запомнить меня! ")
    submit = SubmitField(label="Войти")


class RegistrationForm(FlaskForm):
    username = StringField(
        label="",
        validators=[
            Length(
                3, 20, message="Имя пользователя должно содержать от 1 до 20 символов.",
            ),
            Regexp(
                "^[a-zA-Z0-9]*$",
                message="Имя пользователя должно содержать латинские символы.",
            ),
        ],
        render_kw={
            "data-toggle": "tooltip",
            "title": "Имя пользователя должно содержать только латинские символы и цифры.",
        },
    )
    email = EmailField(label="", validators=[Email(message="Неверный адрес почты.")])
    password = PasswordField(
        label="",
        validators=[
            EqualTo("password2", message="Пароли не совпадают"),
            *password_validators,
        ],
        render_kw={
            "data-toggle": "tooltip",
            "title": "Пароль должен содержать не менее 6 символов, включая цифры, специальные символы и символы в верхнем регистре",
        },
    )
    password2 = PasswordField(label="")
    submit = SubmitField(label="Зарегистрироваться")
