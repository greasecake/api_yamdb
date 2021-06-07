from datetime import datetime as dt
from django.core.exceptions import ValidationError


def year_validator(value):
    if value > dt.now().year:
        raise ValidationError(
            '%(value)s is bigger than the current year',
            params={'value': value}
        )
