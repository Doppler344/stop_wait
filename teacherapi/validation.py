from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_username(username):
    """Простенькая валидация на имя пользователя"""
    UserNameValidator = RegexValidator(
        r"^[A-Za-z][A-Za-z0-9_]{4,29}$",
        message="Имя пользователя:\n1. Начинается с латинского символа\n2. Может включать в себя строчные и заглавные "
                "латинские символы, цифры и знак "
                "_\n3.Длина имени не меньше 5 символов и не больше 30",
    )
    # Пробросит ValidationError в случае несовпадения регулярного выражения
    UserNameValidator(username)

    if User.objects.filter(username=username).exists():
        raise ValidationError('Имя пользователя уже занято')
