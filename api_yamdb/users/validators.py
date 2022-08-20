from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            _(f'{value} служебное имя!')
        )
    elif not re.match(r'[\w.@+-]+\Z', value):
        raise ValidationError(_(f'{value} содержит запрещенные символы!'))
