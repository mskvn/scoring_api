import datetime

from exceptions import ValidationError


class Field:
    def __init__(self, required, nullable):
        self.required = required
        self.nullable = nullable

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, cls):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.name] = value

    def validate(self, value):
        if self.required and value is None:
            raise ValidationError(f'{self.name} is required')
        if not self.nullable and not value:
            raise ValidationError(f'{self.name} should not be empty')


class CharField(Field):

    def validate(self, value):
        super().validate(value)
        if value and not isinstance(value, str):
            raise ValidationError(f'{self.name} must be a str')


class ArgumentsField(Field):

    def validate(self, value):
        super().validate(value)
        if value and not isinstance(value, dict):
            raise ValidationError(f'{self.name} must be a dict')


class EmailField(CharField):

    def validate(self, value):
        super().validate(value)
        if not value:
            return
        if not isinstance(value, str):
            raise ValidationError(f'{self.name} must be a str')
        if '@' not in value:
            raise ValidationError(f'{self.name} must contain @')


class PhoneField(Field):

    def validate(self, value):
        super().validate(value)
        if not value:
            return
        if not isinstance(value, str) and not isinstance(value, int):
            raise ValidationError(f'{self.name} must be a str or int')
        if len(str(value)) != 11:
            raise ValidationError(f'{self.name} length should equal 11')
        if not str(value).startswith('7'):
            raise ValidationError(f'{self.name} should start with 7')


class DateField(Field):
    date_format = '%d.%m.%Y'

    def validate(self, value):
        super().validate(value)
        if not value:
            return
        try:
            datetime.datetime.strptime(value, self.date_format)
        except ValueError:
            raise ValidationError(f"Incorrect date format of {self.name}, should be DD.MM.YYYY")


class BirthDayField(DateField):

    def validate(self, value):
        super().validate(value)
        if not value:
            return
        date = datetime.datetime.strptime(value, self.date_format)
        min_year = datetime.datetime.now().year - 70
        if date.year < min_year:
            raise ValidationError(f"Incorrect {self.name}: year should be more then {min_year}")


class GenderField(Field):

    def validate(self, value):
        super().validate(value)
        if not value:
            return
        valid_values = [0, 1, 2]
        if value not in valid_values:
            raise ValidationError(f'Incorrect {self.name}. Valid values: {valid_values}')


class ClientIDsField(Field):

    def validate(self, value):
        super().validate(value)
        if not value:
            return
        if not isinstance(value, list):
            raise ValidationError(f'{self.name} must be a list')
        if not all(isinstance(x, int) for x in value):
            raise ValidationError(f'All values from {self.name} should be integers')
