import phonenumbers
from wtforms.validators import ValidationError


def validate_phone(form, field):
    try:
        phone = phonenumbers.parse(field.data, "RU")
        if not phonenumbers.is_valid_number(phone):
            raise ValueError()
    except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
        raise ValidationError("Введите ваш номер, с 8 или без.")


def password_is_long(form, field):
    min_legth = 6
    message = f"Пароль должен быть не менее {min_legth} символов."
    if len(field.data) < min_legth:
        raise ValidationError(message)


def has_upper_letters(form, field):
    if not any(map(str.isupper, field.data)):
        raise ValidationError("Пароль должен содержать символы в верхнем регистре.")


def has_digit(form, field):
    if not any(map(str.isdigit, field.data)):
        raise ValidationError("Пароль должен содержать как минимум одну цифру.")


def has_letters(form, field):
    if not any(map(str.isalpha, field.data)):
        raise ValidationError("Пароль должен содержать как минимум одну букву")


def has_special_symbols(form, field):
    special_symbols = '!@#$%^&*()_+=|/?<>~`[]"'
    if not any(symbol in special_symbols for symbol in field.data):
        raise ValidationError(
            "Пароль должен содержать как минимум один специальный символ."
        )


password_validators = [
    password_is_long,
    has_upper_letters,
    has_digit,
    has_letters,
    has_special_symbols,
]
