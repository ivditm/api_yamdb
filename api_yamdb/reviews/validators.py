from django.core.exceptions import ValidationError


import re
import datetime

PATTERN_USER = r'^[\w.@+-]+\Z'
YEAR_VALIDATION_ERROR_MESSAGE = ('Книга не может быть из будущего или '
                                 'выпущена динозаврами')


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Нельзя использовать "me" для имени пользователя'
        )
    elif not re.match(PATTERN_USER, value):
        raise ValidationError(
            'Имя пользователя не соответствует паттерну'
        )
    return value


def validate_year(value):
    if 0 < value <= datetime.datetime.now().year:
        return value
    else:
        raise ValidationError(YEAR_VALIDATION_ERROR_MESSAGE)
