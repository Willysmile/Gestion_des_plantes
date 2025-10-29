from datetime import date
from pydantic import ValidationError


def validate_not_future_date(value: date) -> date:
    """
    Validate that a date is not in the future.
    Raises ValidationError if the date is after today.
    """
    if value > date.today():
        raise ValueError('La date ne peut pas être dans le futur')
    return value
