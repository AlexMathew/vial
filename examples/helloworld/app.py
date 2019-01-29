from definition import app, engine

app.define(models=[], engine=engine)


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
