import datetime
import hashlib
import json
import logging
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser

from handlers import OnlineScoreHandler, ClientsInterestsHandler, BaseRequest
from status_codes import ERRORS, INVALID_REQUEST, INTERNAL_ERROR, NOT_FOUND, BAD_REQUEST, FORBIDDEN, OK
from store import Store

SALT = "Otus"
ADMIN_SALT = "42"
UNKNOWN = 0
MALE = 1
FEMALE = 2
GENDERS = {
    UNKNOWN: "unknown",
    MALE: "male",
    FEMALE: "female",
}


def check_auth(request):
    if request.is_admin:
        msg = (datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).encode('utf-8')
        digest = hashlib.sha512(msg).hexdigest()
    else:
        msg = (request.account + request.login + SALT).encode('utf-8')
        digest = hashlib.sha512(msg).hexdigest()
    if digest == request.token:
        return True
    return False


def method_handler(request, ctx, store):
    methods_map = {
        "online_score": OnlineScoreHandler,
        "clients_interests": ClientsInterestsHandler,
    }
    base_request = BaseRequest(request["body"])
    base_request.validate()
    if not base_request.is_valid():
        return base_request.errors_str(), INVALID_REQUEST
    if not check_auth(base_request):
        return None, FORBIDDEN
    method = methods_map.get(base_request.method)
    if not method:
        return "Method Not Found", NOT_FOUND

    response, code = method().validate_handle(is_admin=base_request.is_admin,
                                              request=method.request_type(base_request.arguments),
                                              ctx=ctx,
                                              store=store)
    return response, code


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }

    store = None

    def get_request_id(self, headers):
        return headers.get('HTTP_X_REQUEST_ID', uuid.uuid4().hex)

    def do_POST(self):
        response, code = {}, OK
        context = {"request_id": self.get_request_id(self.headers)}
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            request = json.loads(data_string)
        except:
            code = BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info("%s: %s %s" % (self.path, data_string, context["request_id"]))
            if path in self.router:
                try:
                    response, code = self.router[path]({"body": request, "headers": self.headers}, context, self.store)
                except Exception as e:
                    logging.exception("Unexpected error: %s" % e)
                    code = INTERNAL_ERROR
            else:
                code = NOT_FOUND

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in ERRORS:
            r = {"response": response, "code": code}
        else:
            r = {"error": response or ERRORS.get(code, "Unknown Error"), "code": code}
        context.update(r)
        logging.info(context)
        self.wfile.write(json.dumps(r).encode('utf-8'))
        return


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8080)
    op.add_option("-a", "--address", action="store", type=str, default='localhost')
    op.add_option("-l", "--log", action="store", default=None)
    op.add_option("--cache_host", action="store", type=str, default='localhost')
    op.add_option("--cache_port", action="store", type=int, default=6379)
    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    store = Store(host=opts.cache_host, port=opts.cache_port)
    MainHTTPHandler.store = store
    server = HTTPServer((opts.address, opts.port), MainHTTPHandler)
    logging.info("Starting server at %s" % opts.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
