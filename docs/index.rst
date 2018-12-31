.. vial documentation master file, created by
   sphinx-quickstart on Mon Dec 24 10:10:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to vial's documentation!
================================

|Maintainability| |Build Status|

Can I build a web app framework using just the in-built ``http.server``
and without pre-existing ORMs?

Introducing **Vial** [because ``flask.__sizeof__()`` >
``bottle.__sizeof__()`` > ``vial.__sizeof__()``]

You can create applications and define database models that this
application will use. These DB models can use of the available DB
engines to run the queries on. As of now, only an engine for PostgreSQL
has been written.

DB engines are organized under ``vial/db`` and are classes derived from
the ``Engine`` class in ``vial.db.base``. They define functionality for
the primary operations - creating a new table and basic CRUD operations
- though it can later be extended to define more complex operations,
like altering the table and operations involving joins.

The base definition of a model (``BaseModel`` in ``vial.orm.model``)
includes functionality for CRUD operations and pagination, which is run
on top of the DB engine specified. The base definition of field
(``BaseField`` in ``vial.orm.field``) includes basic serialization,
which is used when creating the tables. The different field types are
defined in ``vial.orm.types`` - they currently include strings,
integers, floats, booleans and datetime objects. While creating a field
in a model, you can also specify a default value (either as a plain
value or a callable function) and a constraint validator (as a lambda
function that takes as input the value that is to be in that field, and
returns True or False). If no primary key is defined, a serial
incrementing ID is used as primary key.

For example, to create a user model -

.. code:: python

   from vial.orm import types
   from vial.orm.model import BaseModel

   class User(BaseModel):
       _engine = engine
       _application_name = 'sample'

       email = types.Str(not_null=True, unique=True)
       password = types.Str(not_null=True)
       active = types.Bool(default=True)
       created_date = types.Datetime(default=datetime.now)
       job_level = types.Int(constraint=lambda x: x in [1, 2, 3])

Here, ``engine`` is an object of the ``Postgresql`` class and
``'sample'`` is the name of the application (the created table will be
``sample_user``)

Once the models have been defined, the next step is creating the
application and defining all the routes. The application starts as an
object of ``Application`` from ``vial.server.router``. The next step is
associating the models for this application (there is no self-discovery
set up yet) and that is done using the ``define`` method. This is
necessary for the initial set up - creating tables for the models when a
table doesn't already exist. For example,

.. code:: python

   app = Application('example')
   app.define(models=[User, Post])

Routes are defined as decorators for the functions that define the
controller. The decorator takes two arguments - the accepted

.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/4761b904f747f3a500f4/maintainability
   :target: https://codeclimate.com/github/AlexMathew/vial/maintainability
.. |Build Status| image:: https://travis-ci.com/AlexMathew/vial.svg?branch=master
   :target: https://travis-ci.com/AlexMathew/vial


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
