import re
import time
from collections import defaultdict
from http.server import HTTPServer

from .handler import Handler


class Application:
    """
    """
    def __init__(self, app_name, *args, **kwargs):
        self.name = app_name
        self._routes = defaultdict(dict)
        self.models = []

    def __str__(self):
        return f'Application - {self.name}'

    def __repr__(self):
        return f'Application - {self.name}'

    def define(self, models=None, engine=None, *args, **kwargs):
        if not engine:
            raise Exception("DB engine to be used should be specified")

        for model in models:
            model.add_application_instance(self)
            model.use_engine(engine)
            self.models.append(model)

    def route(self, methods, path):
        def decorator(func):
            for method in methods:
                self._routes[method.lower()][path] = func
        return decorator

    def get_controller(self, method, path):
        controller = None
        arguments = tuple()

        for route in self._routes.get(method) or []:
            match = re.search(route, path)
            if match:
                controller = self._routes[method][route]
                arguments = match.groupdict()

        return controller, arguments

    def validate_route(self, command, path):
        routes = defaultdict(list)
        for method, route in self._routes.items():
            for r in route.keys():
                routes[r].append(method)

        acceptable_methods = []
        for route, methods in routes.items():
            if re.match(route, path):
                acceptable_methods.extend(methods)

        if not acceptable_methods:
            return 404

        if command not in acceptable_methods:
            return 405

        return None

    def initialize_db(self):
        for model in self.models or []:
            model.setup()

    def run_server(self, host, port):
        Handler.add_application_instance(self)
        httpd = HTTPServer((host, port), Handler)
        print(time.asctime(), 'Server UP - %s:%s' % (host, port))

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

        httpd.server_close()
        print(time.asctime(), 'Server DOWN - %s:%s' % (host, port))
