***Build the project***

```
docker compose build
```

***Run all services***

```
docker compose up
```

***Make migrations***

```
docker compose exec app python manage.py makemigrations
```

Note: when you start app service, all existing migrations will be applied automatically.

***Run flake8 checks***

```
docker compose exec app flake8
```


***Usage***

***Create superuser to log into django admin***

```
docker compose exec app python manage.py createsuperuser
```

Username field in this project is user's phone number. I made this logic because the communication system-user is made via phone number (SMS | WhatsApp)

***Start a session***

Go to localhost at 8000 port and open the session tab. Then create a session with any user (you should leave all other field blanks. System will fill them during the process of communication with users). Each session have a state which can change or not depending on the user replies.

***State***

1. Name: label for the state
2. Condition: rule to get into the state
3. Enter (Enter Method): Actions to perform, when get into a state
4. States: list of states where session can go depending on the current state

***FSMBuilder***

1. __call__(): this function takes layout from .json file.
2. _build_fsm(): defines which point we should build in our fsm map
3. _build_link_to_top_level_state(): build link to top level states from current state
4. _build_top_level_state(): builds top level state
5. _build_default_node(): ...
