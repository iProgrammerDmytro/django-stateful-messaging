***Build the project***

```
docker-compose build
```

***Run all services***

```
docker-compose up
```

***Make migrations***

```
docker-compose run --rm app sh -c "python manage.py makemigrations"
```

Note: when you start django-app service, all existing migrations are applying automatically.

***Run flake8 checks***

```
docker-compose run --rm app sh -c "flake8"
```