<p align="center">
<img src="https://github.com/Litv1n/fsm/blob/feature/refactor-code/LIMA.png" alt="LIMA" title="LIMA">
 </p>

## Declarative Multi-Channel Conversational Management with Django, Twilio, FSM, Docker, Celery and PostgreSQL

### Flexible SMS and WhatsApp Communication System Based on JSON-Defined FSM Schemas and Twilio Webhooks for Stateful Interactions

This project offers a configurable SMS and WhatsApp communication system, utilizing Django, Twilio, Finite State Machine (FSM), Docker, PostgreSQL, Celery, and webhooks. It enables stateful interactions through JSON-defined schemas, providing a seamless and engaging user experience.

Key Features:

* Declarative communication with JSON-defined FSM schemas: Manage server-user interactions in a readable and flexible way using JSON schemas that define state names, enter methods, conditions for entering states, and possible state transitions.
* Custom parser: Utilize the built-in parser to efficiently process the JSON schema and generate the corresponding FSM structure.
* Twilio webhooks: Leverage Twilio's webhook capabilities to trigger potential changes in session states based on user interactions.
* Docker-based workflow: Streamline development and deployment with Docker containers and Docker Compose for both development and production environments.
* Django admin management: Effortlessly manage users and sessions using the built-in Django admin interface.

By integrating these technologies, this project delivers a robust and user-friendly multi-channel communication platform for stateful conversations through SMS and WhatsApp.

### Example of JSON schema

```
[
  {
    "name": "OPTIN",
    "condition": "get_smth_from_user",
    "enter": "init",
    "states": [
      {
        "name": "OY1",
        "condition": "is_user_reply_yes",
        "enter": "ask_name",
        "states": [
          {
            "name": "@INITBG",
            "condition": "user_reply_name",
            "enter": "greet_user_create_task"
          }
        ]
      },
      {
        "name": "ON1",
        "condition": "is_user_reply_no",
        "enter": "say_np"
      }
    ]
  }
]
```

It is just a sample. This schema can be much more bigger. I made schema for about 100 states and it works as expected in a real project that is in production.

### How to run the project using Docker

The easiest way to run the project is using Docker. It should be installed on your machine.

1. Clone the project
2. Create `.env` file with the following variables:
  - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID.
  - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token.
  - `TWILIO_PHONE_NUMBER`: Your Twilio phone number.
  - `ALLOWED_HOSTS`: A comma-separated list of allowed host/domain names for your Django application (e.g., "localhost,example.com,www.example.com").
3. Run app, databases, and scheduler `docker compose up` or `docker compose up -d`.
4. Create a superuser `docker compose exec app python manage.py createsuperuser` and pass credentials for the superuser.
