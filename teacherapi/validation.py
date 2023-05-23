from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q

from teacherapi.models import Visit


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


def validate_datetime_start_end(start, end):
    if start >= end:
        raise ValidationError('Начало занятия должно быть раньше, чем конец занятия')


def validate_flag_zero_one(flag):
    if flag not in [0, 1]:
        raise ValidationError('Неверный флаг, предполагается 0(Ложь) и 1(Правда)')


def validate_datetime_overlapping(new_start, new_end, office):
    # Проверяем, есть ли уже события, пересекающиеся с новым
    overlapping_events = Visit.objects.filter(
        # начало нового события внутри другого
        Q(datetime_start__lte=new_start, datetime_end__gt=new_start, office=office) |
        # конец нового события внутри другого
        Q(datetime_start__lt=new_end, datetime_end__gte=new_end, office=office) |
        # новое событие внутри другого
        Q(datetime_start__gte=new_start, datetime_end__lte=new_end, office=office)
    )
    if overlapping_events.exists():
        # Обработка случая пересечения событий
        raise ValidationError(f'Занятие пересекается с другими: {[str(event) for event in overlapping_events]}')
