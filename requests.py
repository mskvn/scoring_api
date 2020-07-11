import api
import scoring
from exceptions import ValidationError
from fields import CharField, ArgumentsField, ClientIDsField, DateField, EmailField, GenderField, PhoneField, \
    BirthDayField, Field

ADMIN_LOGIN = "admin"


class RequestMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super(RequestMeta, mcs).__new__(mcs, name, bases, attrs)
        fields = [a for a, v in attrs.items() if isinstance(v, Field)]
        cls.fields = fields
        return cls


class Request(metaclass=RequestMeta):

    def __init__(self, request_body):
        self.request_body = request_body
        self.errors = []

    def is_valid(self):
        return not self.errors

    def validate(self):
        for field in self.fields:
            try:
                setattr(self, field, self.request_body.get(field, None))
            except ValidationError as e:
                self.errors.append(str(e))

    def errors_str(self):
        return ", ".join(self.errors)


class BaseRequest(Request):
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN


class RequestHandler:
    def validate_handle(self, is_admin, request, ctx, store):
        request.validate()
        if not request.is_valid():
            return request.errors_str(), api.INVALID_REQUEST
        return self.handle(is_admin, request, ctx, store)

    def handle(self, is_admin, request, ctx, store):
        return {}, api.OK


class ClientsInterestsRequest(Request):
    client_ids = ClientIDsField(required=True, nullable=False)
    date = DateField(required=False, nullable=True)


class ClientsInterestsHandler(RequestHandler):
    request_type = ClientsInterestsRequest

    def handle(self, is_admin, request, ctx, store):
        clients_interests = dict()
        for cid in request.client_ids:
            clients_interests[str(cid)] = scoring.get_interests(store, cid)
        ctx['nclients'] = len(request.client_ids)
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
            self.errors.append(
                'One of pairs phone-email or first_name-last_name or gender-birthday should not be empty')


class OnlineScoreHandler(RequestHandler):
    request_type = OnlineScoreRequest

    def handle(self, is_admin, request, ctx, store):
        if is_admin:
            score = 42
        else:
            score = scoring.get_score(store,
                                      request.phone,
                                      request.email,
                                      request.birthday,
                                      request.gender,
                                      request.first_name,
                                      request.last_name)

        ctx["has"] = [f for f in request.fields if getattr(request, f) is not None]
        return {"score": score}, api.OK
