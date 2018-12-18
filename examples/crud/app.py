from vial.server.router import Application

from authentication import AuthenticationService
from models import User, Product

app = Application('crud_example')
app.define(models=[User, Product])
auth = AuthenticationService()


@app.route(methods=['GET'], path='/')
def home(request, *args, **kwargs):
    return {
        'message': 'Hello world!'
    }


@app.route(methods=['POST'], path='/signup/$')
def signup(request, *args, **kwargs):
    resp = {
        "status": 400,
        "success": False,
        "message": ""
    }

    try:
        body = request.get_post_body()
        if 'email' not in body or 'password' not in body:
            raise Exception('Request should include email and password')

        if User.get(where={'email': body.get('email')}):
            raise Exception('User with this email already exists')

        User.insert(
            email=body.get('email'),
            password=md5(body.get('password').encode('utf-8')).hexdigest(),
            maintainer=body.get('maintainer') or False,
        )

        resp["status"] = 200
        resp["success"] = True
        resp["message"] = "Success"

    except Exception as e:
        resp['message'] = str(e)

    return resp


@app.route(methods=['POST'], path='/login/$')
def login(request, *args, **kwargs):
    resp = {
        "status": 400,
        "success": False,
        "message": "",
        "user": {}
    }

    try:
        body = request.get_post_body()
        if 'email' not in body or 'password' not in body:
            raise Exception('Request should include email and password')

        user = User.get(where={'email': body.get('email')})

        if not user:
            raise Exception('No user with this email exists')

        if user.get('password') == md5(body.get('password').encode('utf-8')).hexdigest():
            resp["user"] = {
                "id": user.get('id', ''),
                "email": user.get('email', ''),
                "maintainer": user.get('maintainer', ''),
                "auth_token": user.get('auth_token', ''),
            }

            resp["status"] = 200
            resp["success"] = True
            resp["message"] = "Success"

        else:
            resp["status"] = 401
            resp["message"] = "Invalid credentials"

    except Exception as e:
        resp['message'] = str(e)

    return resp


@app.route(methods=['POST'], path='/products/$')
@auth.is_authenticated
def create_product(request, *args, **kwargs):
    resp = {
        "status": 400,
        "success": False,
        "message": "",
    }

    try:
        body = request.get_post_body()
        Product.insert(**body)

        resp["status"] = 200
        resp["success"] = True
        resp["message"] = "Success"

    except Exception as e:
        resp['message'] = str(e)

    return resp


@app.route(methods=['GET'], path='/products/(\?.*)*$')
def list_product(request, *args, **kwargs):
    resp = {
        "status": 400,
        "success": False,
        "message": "",
        "products": [],
    }

    try:
        qs = request.get_query_string()

        resp["products"] = Product.page(
            like={'name': qs.get('name')} if qs.get('name') else None,
            number=int(qs.get('page') or '1'),
            limit=int(qs.get('limit') or '10'),
        )
        resp["status"] = 200
        resp["success"] = True
        resp["message"] = "Success"

    except Exception as e:
        resp['message'] = str(e)

    return resp


@app.route(methods=['GET'], path='/products/(?P<product_code>\d+)/$')
def get_product(request, product_code, *args, **kwargs):
    resp = {
        "status": 400,
        "success": False,
        "message": "",
        "product": {},
    }

    try:
        product = Product.get(where={'code': product_code})

        if not product:
            raise Exception('No product for the given code')

        resp["product"] = product
        resp["status"] = 200
        resp["success"] = True
        resp["message"] = "Success"

    except Exception as e:
        resp['message'] = str(e)

    return resp


@app.route(methods=['PUT', 'PATCH'], path='/products/(?P<product_code>\d+)/$')
@auth.is_authenticated
def update_product(request, product_code, *args, **kwargs):
    resp = {
        "status": 400,
        "success": False,
        "message": "",
    }

    try:
        product = Product.get(where={'code': product_code})

        if not product:
            raise Exception('No product for the given code')

        body = request.get_post_body()
        Product.update(where={'code': product_code}, updation=body)

        resp["status"] = 200
        resp["success"] = True
        resp["message"] = "Success"

    except Exception as e:
        resp['message'] = str(e)

    return resp


@app.route(methods=['DELETE'], path='/products/(?P<product_code>\d+)/$')
@auth.is_authenticated
def delete_product(request, product_code, *args, **kwargs):
    resp = {
        "status": 400,
        "success": False,
        "message": "",
    }

    try:
        product = Product.get(where={'code': product_code})

        if not product:
            raise Exception('No product for the given code')

        Product.delete(where={'code': product_code})

        resp["status"] = 200
        resp["success"] = True
        resp["message"] = "Success"

    except Exception as e:
        resp['message'] = str(e)

    return resp
