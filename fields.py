import datetime


class Field:
    def __init__(self, required, nullable):
        self.required = required
        self.nullable = nullable

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, cls):
        return instance.__dict__.get(self.name)

    def _validate(self, value):
        if self.required and value is None:
            raise ValueError(f'{self.name} is required')
        if not self.nullable and not value:
            raise ValueError(f'{self.name} should not be empty')


class CharField(Field):
    def __init__(self, required, nullable):
        super().__init__(required, nullable)

    def __set__(self, instance, value):
        super()._validate(value)
        if value:
            if not isinstance(value, str):
                raise TypeError('Must be a str')
        instance.__dict__[self.name] = value


class ArgumentsField(Field):
    def __init__(self, required, nullable):
        super().__init__(required, nullable)

    def __set__(self, instance, value):
        super()._validate(value)
        if value:
            if not isinstance(value, dict):
                raise TypeError('Must be a dict')
        instance.__dict__[self.name] = value


class EmailField(CharField):
    def __init__(self, required, nullable):
        super().__init__(required, nullable)

    def __set__(self, instance, value):
        super()._validate(value)
        if value:
            if not isinstance(value, str):
                raise TypeError('Must be a str')
            if '@' not in value:
                raise ValueError('Value must contain @')
        instance.__dict__[self.name] = value


class PhoneField(Field):
    def __init__(self, required, nullable):
        super().__init__(required, nullable)

    def __set__(self, instance, value):
        if value:
            if not isinstance(value, str) or not isinstance(value, int):
                raise TypeError('Must be a str or int')
            if len(str(value)) != 11:
                raise ValueError('Values length should equal 11')
            if not str(value).startswith('7'):
                raise ValueError('Values should start with 7')
        instance.__dict__[self.name] = value


class DateField(Field):
    def __init__(self, required, nullable):
        super().__init__(required, nullable)

    def _validate(self, value):
        super()._validate(value)
        if value:
            try:
                return datetime.datetime.strptime(value, '%d-%m-%Y')
            except ValueError:
                raise ValueError("Incorrect date format, should be YYYY.MM.DD")

    def __set__(self, instance, value):
        date = self._validate(value)
        instance.__dict__[self.name] = date


class BirthDayField(DateField):
    def __init__(self, required, nullable):
        super().__init__(required, nullable)

    def __set__(self, instance, value):
        date = super()._validate(value)
        if date:
            min_year = datetime.datetime.now().year - 70
            if date.year > min_year:
                raise ValueError(f"Incorrect date: year should be more then {min_year}")
        instance.__dict__[self.name] = date


class GenderField(Field):
    def __init__(self, required, nullable):
        super().__init__(required, nullable)

    def __set__(self, instance, value):
        super()._validate(value)
        if value:
            valid_values = [0, 1, 2]
            if value not in valid_values:
                raise ValueError(f'Incorrect gender. Valid values: {valid_values}')
        instance.__dict__[self.name] = value


class ClientIDsField(Field):
    def __init__(self, required, nullable):
        super().__init__(required, nullable)

    def __set__(self, instance, value):
        super()._validate(value)
        if value:
            if not isinstance(value, list):
                raise TypeError('Must be a list')
        instance.__dict__[self.name] = value
