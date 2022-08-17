from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            _(f'{value} is forbidden username!')
<<<<<<< HEAD
        )
=======
        )
>>>>>>> 5638cbd... Merge pull request #8 from epsilonm/feature/get_permissions
