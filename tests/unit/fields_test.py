import unittest

from fields import CharField, ArgumentsField, EmailField, PhoneField, DateField, \
    BirthDayField, GenderField, ClientIDsField
from tests.decorators import cases


class FieldsTest(unittest.TestCase):

    def test_char_field_positive(self):
        class Test:
            char_field = CharField(required=True, nullable=False)

        test = Test()
        actual_value = 'string'
        test.char_field = actual_value
        self.assertEqual(test.char_field, actual_value)

    @cases([
        {'field': {'required': True, 'value': None}, 'error': 'char_field is required'},
        {'field': {'nullable': False, 'value': None}, 'error': 'char_field should not be empty'},
        {'field': {'nullable': False, 'value': ''}, 'error': 'char_field should not be empty'},
        {'field': {'value': 123}, 'error': 'char_field must be a str'},
    ])
    def test_char_field_negative(self, test_data):
        class Test:
            char_field = CharField(required=test_data['field'].get('required', False),
                                   nullable=test_data['field'].get('nullable', True))

        test = Test()
        with self.assertRaises(Exception) as exp:
            test.char_field = test_data['field'].get('value', 'test')

        self.assertEqual(test_data['error'], str(exp.exception))

    def test_arguments_field_positive(self):
        class Test:
            arg_field = ArgumentsField(required=True, nullable=False)

        test = Test()
        actual_value = {'key': 'value'}
        test.arg_field = actual_value
        self.assertEqual(test.arg_field, actual_value)

    @cases([
        {'field': {'required': True, 'value': None}, 'error': 'arg_field is required'},
        {'field': {'nullable': False, 'value': None}, 'error': 'arg_field should not be empty'},
        {'field': {'nullable': False, 'value': {}}, 'error': 'arg_field should not be empty'},
        {'field': {'value': 'string'}, 'error': 'arg_field must be a dict'},
    ])
    def test_arguments_field_negative(self, test_data):
        class Test:
            arg_field = ArgumentsField(required=test_data['field'].get('required', False),
                                       nullable=test_data['field'].get('nullable', True))

        test = Test()
        with self.assertRaises(Exception) as exp:
            test.arg_field = test_data['field'].get('value', {'key': 'value'})

        self.assertEqual(test_data['error'], str(exp.exception))

    def test_email_field_positive(self):
        class Test:
            email_field = EmailField(required=True, nullable=False)

        test = Test()
        actual_value = 'user@domain'
        test.email_field = actual_value
        self.assertEqual(test.email_field, actual_value)

    @cases([
        {'field': {'required': True, 'value': None}, 'error': 'email_field is required'},
        {'field': {'nullable': False, 'value': None}, 'error': 'email_field should not be empty'},
        {'field': {'nullable': False, 'value': ''}, 'error': 'email_field should not be empty'},
        {'field': {'value': 123}, 'error': 'email_field must be a str'},
        {'field': {'value': 'user%domain'}, 'error': 'email_field must contain @'},
    ])
    def test_email_field_negative(self, test_data):
        class Test:
            email_field = EmailField(required=test_data['field'].get('required', False),
                                     nullable=test_data['field'].get('nullable', True))

        test = Test()
        with self.assertRaises(Exception) as exp:
            test.email_field = test_data['field'].get('value', {'key': 'value'})

        self.assertEqual(test_data['error'], str(exp.exception))

    @cases(['79991234567', 79991234567])
    def test_phone_field_positive(self, valid_phone):
        class Test:
            phone_field = PhoneField(required=True, nullable=False)

        test = Test()
        test.phone_field = valid_phone
        self.assertEqual(test.phone_field, valid_phone)

    @cases([
        {'field': {'required': True, 'value': None}, 'error': 'phone_field is required'},
        {'field': {'nullable': False, 'value': None}, 'error': 'phone_field should not be empty'},
        {'field': {'value': {'phone': 79991234567}}, 'error': 'phone_field must be a str or int'},
        {'field': {'value': 89991234567}, 'error': 'phone_field should start with 7'},
        {'field': {'value': '89991234567'}, 'error': 'phone_field should start with 7'},
        {'field': {'value': '799912345678'}, 'error': 'phone_field length should equal 11'},
        {'field': {'value': 799912345678}, 'error': 'phone_field length should equal 11'},
        {'field': {'value': 7999123456}, 'error': 'phone_field length should equal 11'},
    ])
    def test_phone_field_negative(self, test_data):
        class Test:
            phone_field = PhoneField(required=test_data['field'].get('required', False),
                                     nullable=test_data['field'].get('nullable', True))

        test = Test()
        with self.assertRaises(Exception) as exp:
            test.phone_field = test_data['field'].get('value', {'key': 'value'})

        self.assertEqual(test_data['error'], str(exp.exception))

    def test_date_field_positive(self):
        class Test:
            date_field = DateField(required=True, nullable=False)

        valid_date = '01.01.1970'
        test = Test()
        test.date_field = valid_date
        self.assertEqual(test.date_field, valid_date)

    @cases([
        {'field': {'required': True, 'value': None}, 'error': 'date_field is required'},
        {'field': {'nullable': False, 'value': None}, 'error': 'date_field should not be empty'},
        {'field': {'value': 123}, 'error': 'date_field must be a str'},
        {'field': {'value': '01-01-1970'}, 'error': 'Incorrect date format of date_field, should be DD.MM.YYYY'},
        {'field': {'value': '01/01/1970'}, 'error': 'Incorrect date format of date_field, should be DD.MM.YYYY'},
    ])
    def test_date_field_negative(self, test_data):
        class Test:
            date_field = DateField(required=test_data['field'].get('required', False),
                                   nullable=test_data['field'].get('nullable', True))

        test = Test()
        with self.assertRaises(Exception) as exp:
            test.date_field = test_data['field'].get('value', {'key': 'value'})

        self.assertEqual(test_data['error'], str(exp.exception))

    def test_birthday_field_positive(self):
        class Test:
            birthday_field = BirthDayField(required=True, nullable=False)

        valid_birthday = '01.01.1970'
        test = Test()
        test.birthday_field = valid_birthday
        self.assertEqual(test.birthday_field, valid_birthday)

    @cases([
        {'field': {'required': True, 'value': None}, 'error': 'birthday_field is required'},
        {'field': {'nullable': False, 'value': None}, 'error': 'birthday_field should not be empty'},
        {'field': {'value': 123}, 'error': 'birthday_field must be a str'},
        {'field': {'value': '01.01.1900'}, 'error': 'Incorrect birthday_field: year should be more then 1950'},
    ])
    def test_birthday_field_negative(self, test_data):
        class Test:
            birthday_field = BirthDayField(required=test_data['field'].get('required', False),
                                           nullable=test_data['field'].get('nullable', True))

        test = Test()
        with self.assertRaises(Exception) as exp:
            test.birthday_field = test_data['field'].get('value', {'key': 'value'})

        self.assertEqual(test_data['error'], str(exp.exception))

    @cases([0, 1, 2])
    def test_gender_field_positive(self, valid_gender):
        class Test:
            gender_field = GenderField(required=True, nullable=False)

        test = Test()
        test.gender_field = valid_gender
        self.assertEqual(test.gender_field, valid_gender)

    @cases([
        {'field': {'required': True, 'value': None}, 'error': 'gender_field is required'},
        {'field': {'nullable': False, 'value': None}, 'error': 'gender_field should not be empty'},
        {'field': {'value': 3}, 'error': 'Incorrect gender_field. Valid values: [0, 1, 2]'},
        {'field': {'value': '3'}, 'error': 'Incorrect gender_field. Valid values: [0, 1, 2]'},
    ])
    def test_gender_field_negative(self, test_data):
        class Test:
            gender_field = GenderField(required=test_data['field'].get('required', False),
                                       nullable=test_data['field'].get('nullable', True))

        test = Test()
        with self.assertRaises(Exception) as exp:
            test.gender_field = test_data['field'].get('value', {'key': 'value'})

        self.assertEqual(test_data['error'], str(exp.exception))

    def test_client_id_field_positive(self):
        class Test:
            client_id_field = ClientIDsField(required=True, nullable=False)

        test = Test()
        valid_client_ids = [1, 2, 3]
        test.client_id_field = valid_client_ids
        self.assertEqual(test.client_id_field, valid_client_ids)

    @cases([
        {'field': {'required': True, 'value': None}, 'error': 'client_ids_field is required'},
        {'field': {'nullable': False, 'value': None}, 'error': 'client_ids_field should not be empty'},
        {'field': {'value': '1,2,3'}, 'error': 'client_ids_field must be a list'},
        {'field': {'value': [1, 2, '3']}, 'error': 'All values from client_ids_field should be integers'},
    ])
    def test_client_id_field_negative(self, test_data):
        class Test:
            client_ids_field = ClientIDsField(required=test_data['field'].get('required', False),
                                              nullable=test_data['field'].get('nullable', True))

        test = Test()
        with self.assertRaises(Exception) as exp:
            test.client_ids_field = test_data['field'].get('value', {'key': 'value'})

        self.assertEqual(test_data['error'], str(exp.exception))
