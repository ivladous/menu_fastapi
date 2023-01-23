# Restaurant menu REST API

**Menus, submenus and dishes**

*Python 3.10+*

*PostgreSQL*


*Docs at http://localhost:8000/docs*

## Run app in Docker

```commandline
docker-compose up -d 
```

## Run tests in Docker

```commandline
 docker compose -f .\tests-docker-compose.yml up
```

## Install without Docker

```commandline
python -m venv venv
```
```commandline
. ./venv/Scripts/activate
```
```commandline
pip install -r requirements.txt
```
```commandline
alembic upgrade head
```
```commandline
uvicorn main:app
```
