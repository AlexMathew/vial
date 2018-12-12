# An overview of the project

## tl;dr

* `vial` handles setting up the web app and the database abstractions.
* `run.py` offers a command line interface to set up tables and start the web server for any given project.
* The `hellofresh` directory includes the app definition for the Recipes API.
* The project can be run with `docker-compose up` (it runs at `localhost:8080` but the port can be changed in the `SERVER_PORT` variable in `ops/environment`)
* Basic tests have been set up, which can be run with `nosetests -v`

## The whole picture

### Vial

The primary goal was abstracting the web server routing and database interactions. Introducing **Vial** [because `flask.__sizeof__()` > `bottle.__sizeof__()` > `vial.__sizeof__()`]

You can create applications and define database models that this application will use. These DB models can use of the available DB engines to run the queries on. As of now, only an engine for PostgreSQL has been written. 

DB engines are organized under `vial/db` and are classes derived from the `Engine` class in `vial.db.base`. They define functionality for the primary operations - creating a new table and basic CRUD operations - though it can later be extended to define more complex operations, like altering the table and operations involving joins. 

The base definition of a model (`BaseModel` in `vial.orm.model`) includes functionality for CRUD operations and pagination, which is run on top of the DB engine specified. The base definition of field (`BaseField` in `vial.orm.field`) includes basic serialization, which is used when creating the tables. The different field types are defined in `vial.orm.types` - they currently include strings, integers, floats, booleans and datetime objects. While creating a field in a model, you can also specify a default value (either as a plain value or a callable function) and a constraint validator (as a lambda function that takes as input the value that is to be in that field, and returns True or False). If no primary key is defined, a serial incrementing ID is used as primary key.

For example, to create a user model - 

```python
class User(BaseModel):
    _engine = engine
    _application_name = 'sample'

    email = types.Str(not_null=True, unique=True)
    password = types.Str(not_null=True)
    active = types.Bool(default=True)
    created_date = types.Datetime(default=datetime.now)
    job_level = type.Int(constraint=lambda x: x in [1, 2, 3])
```

Here, `engine` is an object of the `Postgresql` class and `'sample'` is the name of the application (the created table will be `sample_user`)

Once the models have been defined, the next step is creating the application and defining all the routes. The application starts as an object of `Application` from `vial.server.router`. The next step is associating the models for this application (there is no self-discovery set up yet) and that is done using the `define` method. This is necessary for the initial set up - creating tables for the models when a table doesn't already exist. For example,

```python
app = Application('hellofresh')
app.define(models=[User, Recipe]) # User & Recipe are defined in models.py
```

Routes are defined as decorators for the functions that define the controller. The decorator takes two arguments - the accepted HTTP methods for that view, and a regular expression for the accepted path. If the view takes parameters, the regex can include these parameters - for example, `(?P<user_id>\d+)`. For GET requests that take a query string, that will have to be specified in the regex - `(\?.*)*$`

An example view would look like this.

```python
@app.route(methods=['GET'], path='/')
def home(request, *args, **kwargs):
    return {
        'message': 'Hello world!'
    }
```

The running web server uses `Handler` from `vial.server.handler` as its request handler (derived from `BaseHTTPRequestHandler`) and this handles all of the incoming HTTP requests. The `handle_http()` method validates the path of the request and runs the corresponding controller. This class also includes `get_post_body()` and `get_query_string()` which can be used in POST and GET requests, respectively.

Vial also includes a CLI to initialize the project (set up the tables) and run the web server. 

```
Usage:
    run.py (-h | --help | --version)
    run.py initialize <app>
    run.py server <app>
```

The `<app>` specifies the application to be run. There are requirements to the project structure to make this set up work. The application should live in a module of its own, and should include an `app.py` where the primary bulk of the logic resides. The minimum requirement in `app.py` is that it should define the `initialize_db()` and `run_server()` which is what is called from the CLI commands.

As a summary, an application should (at the minimum) look like this - 

```
- sample
|
 - __init__.py
 - app.py
```

### The Recipes API

With the abstractions to create and define the application set, creating the required API is fairly straightforward. The `hellofresh` module contains the implementation of this API. `models.py` defines the `User` and `Recipe` models. `app.py` defines the application, and all the routes point to the corresponding controllers for the various CRUD operations. The ratings for the recipes are stored in Redis (a helper wrapper is defined in `hellofresh.helpers.redis`). Authentication is implemented using bearer tokens. When a row is created for `User`, a random hash string is stored, which is used as the auth token. An `AuthenticationService` is defined in `hellofresh.services.authentication`, which includes the `is_authenticated_request` decorator, that looks for the bearer token in the `Authorization` header and validates if this is the auth token of a user with maintainer access. 

As an example of something that sums all of this up, the controller to create a new recipe - 
```python
@app.route(methods=['POST'], path='/recipes/$')
@auth.is_authenticated_request
def create_recipe(request, *args, **kwargs):
    resp = {
        "status": 400,
        "success": False,
        "message": "",
    }

    try:
        body = request.get_post_body()
        Recipe.insert(**body)

        resp["status"] = 200
        resp["success"] = True
        resp["message"] = "Success"

    except Exception as e:
        resp['message'] = str(e)

    return resp

```

### Limitations and future improvements

* Joins have to be implemented, right from the DB engine level.
* No provision to define foreign keys.
* Cleaner regular expressions to define the routes, especially the GET query string case.
* No ability for handling DB migrations.
