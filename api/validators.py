from datetime import datetime as dt


def year_validator(value):
    if value > dt.now().year:
        raise ValidationError(
            '%(value)s is bigger than the current year',
            params={'value': value}
        )