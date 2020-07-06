import inspect

import api
import scoring
from fields import CharField, ArgumentsField, ClientIDsField, DateField, EmailField, GenderField, PhoneField, \
    BirthDayField
from exceptions import ValidationError

ADMIN_LOGIN = "admin"


class Request:
    def __init__(self, request_body):
        self._request_body = request_body
        self._errors = []
        self._fields = []
        self._init_request_fields(['is_admin'])

    def is_valid(self):
        return len(self._errors) == 0

    def validate(self):
        for field in self._fields:
            try:
                setattr(self, field, self._request_body.get(field, None))
            except ValidationError as e:
                self._errors.append(str(e))

    def _init_request_fields(self, exclude_fields):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        self._fields = [a[0] for a in attributes if not a[0].startswith('_') and a[0] not in exclude_fields]

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


class ClientsInterestsHandler:

    def __init__(self, request_body):
        self.request = ClientsInterestsRequest(request_body)

    def do_request(self, is_admin, ctx, store):
        clients_interests = dict()
        for cid in self.request.client_ids:
            clients_interests[str(cid)] = scoring.get_interests(store, cid)
        ctx['nclients'] = len(self.request.client_ids)
        return clients_interests, api.OK


class OnlineScoreRequest(Request):
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)

    def validate(self):
        super().validate()
        if not (
                (self.phone is not None and self.email is not None) or
                (self.first_name is not None and self.last_name is not None) or
                (self.gender is not None and self.birthday is not None)
        ):
            self._errors.append(
                'One of pairs phone-email or first_name-last_name or gender-birthday should not be empty')


class OnlineScoreHandler:

    def __init__(self, request_body):
        self.request = OnlineScoreRequest(request_body)

    def do_request(self, is_admin, ctx, store):
        if is_admin:
            score = 42
        else:
            score = scoring.get_score(store,
                                      self.request.phone,
                                      self.request.email,
                                      self.request.birthday,
                                      self.request.gender,
                                      self.request.first_name,
                                      self.request.last_name)

        ctx["has"] = [f for f in self.request._fields if getattr(self.request, f) is not None]
        return {"score": score}, api.OK
