from vial.db.sql.postgresql import Postgresql
from vial.server.application import Application

app = Application('crud_example')

engine = Postgresql(
    dbname=os.getenv('POSTGRES_DATABASE'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT')
)
