from django.core.exceptions import ValidationError
from datetime import datetime


def validate_integer(value):
    if value < 0:
        raise ValidationError("You can not enter a negative value")
    else:
        return value


def validate_date(value):
    if value < datetime.now().date():
        raise ValidationError("Date can not be before current date")
    else:
        return value


def validate_status(value):
    if value not in ["Draft", "Active Recruitment", "Recruitment Ended"]:
        raise ValidationError("Invalid status")
    else:
        return value


def clean(self):
    cleaned_data = super().clean()
    startdate = cleaned_data.get("recruitmentStartDate")
    enddate = cleaned_data.get("recruitmentEndDate")
    if startdate and enddate and (enddate < startdate):
        msg = u"Trial end date should be greater than trial start date."
        raise forms.ValidationError(msg, code="invalid")
