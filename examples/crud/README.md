# Example - CRUD API

This example is designed to define a simple CRUD API.

* The `User` model keeps new users on signup and auto-generates an auth token for the user. The login endpoint returns this auth token. The other endpoints use this bearer token for authentication.
* The `Product` model is the basis for all the CRUD endpoints.

To try out the application, you can start it with `$ docker-compose up --build` - this starts a Postgres container and an application container that runs the `vial` server after initializing the models (which creates the tables in the DB).

The endpoints available are:

* Signup

```bash
curl --request POST \
  --url http://localhost:9000/signup/ \
  --header 'content-type: application/json' \
  --data '{
	"email": "johndoe@example.com",
	"password": "password",
	"maintainer": true
}'
```

```javascript
{
  "status": 200,
  "success": true,
  "message": "Success"
}
```

* Login

```bash
curl --request POST \
  --url http://localhost:9000/login/ \
  --header 'content-type: application/json' \
  --data '{
	"email": "johndoe@example.com",
	"password": "password"
}'
```

```javascript
{
  "status": 200,
  "success": true,
  "message": "Success",
  "user": {
    "id": 2,
    "email": "johndoe@example.com",
    "maintainer": true,
    "auth_token": "7f0821b2d56fe7653e2b07b3a7f27514"
  }
}
```

* Create product

```bash
curl --request POST \
  --url http://localhost:9000/products/ \
  --header 'authorization: Bearer 7f0821b2d56fe7653e2b07b3a7f27514' \
  --header 'content-type: application/json' \
  --data '{
	"code": "A1B",
	"name": "Product1",
	"description": "This is Product1",
	"category": 1
}'
```

```javascript
{
  "status": 200,
  "success": true,
  "message": "Success"
}
```

* List products (with search and pagination)

```bash
curl --request GET \
  --url 'http://localhost:9000/products/?limit=1&page=1&name=prod'
```

```javascript
{
  "status": 200,
  "success": true,
  "message": "Success",
  "products": [
    {
      "code": "A1B",
      "name": "Product1",
      "description": "This is Product1",
      "category": 1,
      "created_date": "2018-12-19T08:51:52.726062"
    }
  ]
}
```

* Get product

```bash
curl --request GET \
  --url http://localhost:9000/products/A1B/
```

```javascript
{
  "status": 200,
  "success": true,
  "message": "Success",
  "product": {
    "code": "A1B",
    "name": "Product1",
    "description": "This is Product1",
    "category": 1,
    "created_date": "2018-12-19T08:51:52.726062"
  }
}
```

* Update product

```bash
curl --request PATCH \
  --url http://localhost:9000/products/A1B/ \
  --header 'authorization: Bearer 7f0821b2d56fe7653e2b07b3a7f27514' \
  --header 'content-type: application/json' \
  --data '{
	"category": 2
}'
```

```javascript
curl --request PATCH \
  --url http://localhost:9000/products/A1B/ \
  --header 'authorization: Bearer 7f0821b2d56fe7653e2b07b3a7f27514' \
  --header 'content-type: application/json' \
  --data '{
	"category": 2
}'
```

* Delete product

```bash
curl --request DELETE \
  --url http://localhost:9000/products/A1B/ \
  --header 'authorization: Bearer 7f0821b2d56fe7653e2b07b3a7f27514'
```

```javascript
{
  "status": 200,
  "success": true,
  "message": "Success"
}
```
