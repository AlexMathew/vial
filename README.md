# Vial

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7583124ac88f42e3b12ea95c0b797df0)](https://app.codacy.com/app/AlexMathew/vial?utm_source=github.com&utm_medium=referral&utm_content=AlexMathew/vial&utm_campaign=Badge_Grade_Settings)
[![Maintainability](https://api.codeclimate.com/v1/badges/4761b904f747f3a500f4/maintainability)](https://codeclimate.com/github/AlexMathew/vial/maintainability)
[![Build Status](https://travis-ci.com/AlexMathew/vial.svg?branch=master)](https://travis-ci.com/AlexMathew/vial)

Can I build a web app framework using just the in-built `http.server` and without pre-existing ORMs?

Introducing **Vial** [because `flask.__sizeof__()` > `bottle.__sizeof__()` > `vial.__sizeof__()`]

You can create applications and define database models that this application will use. These DB models can use of the available DB engines to run the queries on. As of now, only an engine for PostgreSQL has been written.

DB engines are organized under `vial/db` and are classes derived from the `Engine` class in `vial.db.base`. They define functionality for the primary operations - creating a new table and basic CRUD operations - though it can later be extended to define more complex operations, like altering the table and operations involving joins.

The base definition of a model (`BaseModel` in `vial.orm.model`) includes functionality for CRUD operations and pagination, which is run on top of the DB engine specified. The base definition of field (`BaseField` in `vial.orm.field`) includes basic serialization, which is used when creating the tables. The different field types are defined in `vial.orm.types` - they currently include strings, integers, floats, booleans and datetime objects. While creating a field in a model, you can also specify a default value (either as a plain value or a callable function) and a constraint validator (as a lambda function that takes as input the value that is to be in that field, and returns True or False). If no primary key is defined, a serial incrementing ID is used as primary key.

For example, to create a user model -

```python
from vial.orm import types
from vial.orm.model import BaseModel

class User(BaseModel):
    email = types.Str(not_null=True, unique=True)
    password = types.Str(not_null=True)
    active = types.Bool(default=True)
    created_date = types.Datetime(default=datetime.now)
    job_level = types.Int(constraint=lambda x: x in [1, 2, 3])
```

Once the models have been defined, the next step is creating the application and defining all the routes. The application starts as an object of `Application` from `vial.server.application`. The next step is associating the models for this application (there is no self-discovery set up yet) and that is done using the `define` method. This is necessary for the initial set up - creating tables for the models when a table doesn't already exist. For example,

```python
from vial.server.application import Application

app = Application('example')
app.define(models=[User, Post], engine=engine)
```

Here, `engine` is an object of the `Postgresql` class and `'example'` is the name of the application (the created tables after set up will be `example_user` and `example_post`)

Routes are defined as decorators for the functions that define the controller. The decorator takes two arguments - the accepted HTTP methods for that view, and a regular expression for the accepted path. Like any regular expression, the `^` denotes the start of the string and the `$` denotes the end of the string. If the view takes parameters, the regex can include these parameters - for example, `(?P<user_id>\d+)`. There are helpers available for common URL features. For example, for GET requests that take a query string, you can specify `<qs>` for the query string.

An example view would look like this.

```python
@app.route(methods=['GET'], path='/$')
def home(request, *args, **kwargs):
    return {
        'message': 'Hello world!'
    }

@app.route(methods=['GET'], path='/<qs>$')
def query(request, *args, **kwargs):
    qs = request.get_query_string()

    return {
        'query': qs
    }
```

The running web server uses `Handler` from `vial.server.handler` as its request handler (derived from `BaseHTTPRequestHandler`) and this handles all of the incoming HTTP requests. The `handle_http()` method validates the path of the request and runs the corresponding controller. This class also includes `get_post_body()` and `get_query_string()` which can be used in POST and GET requests, respectively.

Vial also includes a CLI to initialize the project (set up the tables) and run the web server.

```bash
Usage:
    vial (-h | --help | --version)
    vial initialize
    vial server [--host=<host>] [--port=<port>]

Options:
    -h, --help
        Show this help message and exit
    --version, -V
        Display the version of Vial
    --host=<host>, -H <host>
        Specifies the host name to run on [default: 127.0.0.1]
    --port=<port>, -P <port>
        Specifies the port to run on [default: 8000]
```

The app in the current directory is run. There are requirements to the project structure to make this set up work. The application should live in a module of its own, and should include an `app.py` where the primary bulk of the logic resides.

As a summary, an application should (at the minimum) look like this -

```bash
- sample
|
 - __init__.py
 - app.py
```

## Limitations and future improvements

* Joins have to be implemented, right from the DB engine level.
* No provision to define foreign keys.
* Cleaner regular expressions to define the routes, especially the GET query string case.
* No ability for handling DB migrations.
