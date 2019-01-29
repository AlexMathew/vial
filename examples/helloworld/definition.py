from vial.db.sql.sqlite import Sqlite
from vial.server.application import Application

app = Application('helloworld')

engine = Sqlite(
    dbname='helloworld'
)
