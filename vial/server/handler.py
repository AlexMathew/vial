import datetime
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)


class Handler(BaseHTTPRequestHandler):
    _application = None

    @classmethod
    def add_application_instance(cls, application):
        cls._application = application

    def __str__(self):
        return f'Handler - {self._application}'

    def __repr__(self):
        return f'Handler - {self._application}'

    def get_post_body(self):
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        return message

    def get_query_string(self):
        return dict(part.split('=') for part in urlparse(self.path).query.split('&') or [] if part)

    def handle_http(self):
        status = 500
        content_type = 'application/json'
        error = self._application.validate_route(self.command.lower(), self.path)

        if error:
            error_text = {
                404: '404 Not Found',
                405: '405 Invalid Method',
            }

            content = error_text.get(error) or ''
            status = error
            content_type = 'text/plain'

        else:
            controller, arguments = self._application.get_controller(
                method=self.command.lower(),
                path=self.path
            )
            content = controller(request=self, **arguments)
            status = content.get('status') or 400

        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        return bytes(json.dumps(content), "UTF-8")

    def respond(self):
        content = self.handle_http()
        self.wfile.write(content)


HTTP_VERBS = ['HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE']
for verb in HTTP_VERBS:
    setattr(Handler, f'do_{verb}', lambda self: self.respond())
