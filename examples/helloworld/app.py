from vial.server.application import Application

app = Application('helloworld')


@app.route(methods=['GET'], path='/')
def home(request, *args, **kwargs):
    return {
        'message': 'Hello world!'
    }
