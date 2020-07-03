import inspect

from fields import *

ADMIN_LOGIN = "admin"


class Request:
    def __init__(self, request_body):
        self._request_body = request_body
        self._errors = []
        self._base_validate()

    def is_valid(self):
        return len(self._errors) == 0

    def _base_validate(self):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        fields = [a for a in attributes if not ('_' in a[0])]
        for field, _ in fields:
            try:
                setattr(self, field, self._request_body.get(field, None))
            except (ValueError, TypeError) as e:
                self._errors.append(str(e))

    def errors_str(self):
        return ", ".join(self._errors)


class BaseRequest(Request):
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN


class ClientsInterestsRequest(Request):
    client_ids = ClientIDsField(required=True, nullable=False)
    date = DateField(required=False, nullable=True)

    def do_request(self):
        pass


class OnlineScoreRequest(Request):
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)

    def __init__(self, request_body):
        super().__init__(request_body)
        self._validate()

    def _validate(self):
        if not ((self.phone and self.email) or (self.first_name and self.last_name) or (self.gender and self.birthday)):
            self._errors.append('One of pairs phone-email or first_name-last_name or gender-birthday')

    def do_request(self):
        pass
