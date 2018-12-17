from vial.server.router import Application

from models import User, Product

app = Application('crud_example')
app.define(models=[User, Product])


@app.route(methods=['GET'], path='/')
def home(request, *args, **kwargs):
    return {
        'message': 'Hello world!'
    }
