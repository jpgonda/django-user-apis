# django-user-apis

## Setup
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cd mynewsite
python manage.py migrate
```

## Run server
```
python manage.py runserver
```

## Available APIs
Create new user
```
curl -X POST \
  http://127.0.0.1:8000/users/ \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "myemail@email.com",
    "password": "hello"
}'
```

Validate user using token
```
curl -X PUT \
  http://127.0.0.1:8000/users/key/ \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
	"token": "468f0ce14d3e64776acff2bdc8daa0c3dffbe6f02"
}'
```

Generate token for auth
```
curl -X POST \
  http://127.0.0.1:8000/oauth-token/ \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
	"username": "myemail@email.com",
	"password": "hello"
}'
```

Get all the users. Response changes based on validity of the token supplied
```
curl -X GET \
  http://127.0.0.1:8000/users/ \
  -H 'Authorization: Bearer 29074ef9a4347ac28fdc65914102da5980b4096e' \
  -H 'Cache-Control: no-cache'
```

Change password of a user based on the given bearer token
```
curl -X PUT \
  http://127.0.0.1:8000/users/password/ \
  -H 'Authorization: Bearer 29074ef9a4347ac28fdc65914102da5980b4096e' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
    "new_password": "hello2!",
    "password": "hello"
}'
```