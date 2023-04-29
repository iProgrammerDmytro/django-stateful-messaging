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
3. `docker compose up` to see logs or `docker compose up -d` ro tun in a background.
4. Create a superuser `docker compose exec app python manage.py createsuperuser` and pass credentials for the superuser.
5. Go to the `http://localhost:8000/admin/`.

### How to tweak the project for your own uses

To create your own FSM tree, you will need to follow these steps:

1. Create a JSON schema in the `app/modules/module_schema` folder
2. Define enter methods and conditions for each state in the schema
3. Pass the paths to your schema, enter methods, and conditions files in the `signals.py` file
4. Implement custom scheduled tasks using the `TaskCreator` (optional)
5. Configure email notifications (optional)

1) Create a JSON Schema in the `app/modules/module_schema` folder

Begin by creating a JSON file that defines your desired FSM tree. This file should be placed in the `app/modules/module_schema` folder. Name your JSON schema file descriptively, following the format of the existing schema files, such as `sample_schema.json`.

The JSON schema should define state names, enter methods, conditions for entering states, and possible state transitions. State transitions specify which states the FSM can move to from the current state.

2) Define Enter Methods and Conditions for Each State

For each state in your JSON schema, create corresponding enter methods and conditions. These methods should be defined in separate files named `enter_methods.py` and `conditions.py`, which should be saved within a folder for your module in the `app/modules` directory.

Ensure that the method names in `enter_methods.py` and `conditions.py` match the enter and condition properties of the corresponding state objects in the JSON schema.

3) Pass the Paths to Your Schema, Enter Methods, and Conditions Files in the `signals.py` file

To link your custom JSON schema, enter methods, and conditions to the FSM implementation, you need to pass the paths to these files in the `signals.py` file.

For example, if you have the following module structure:

```
app/modules
├── module_schema
│   └── sample_schema.json
└── your_module_name
    ├── __init__.py
    ├── conditions.py
    ├── enter_methods.py
    └── ... (other optional files)
```

You will need to pass the following paths in the signals.py file:

* JSON schema: `app/modules/module_schema/your_schema_name.json`
* Enter methods: `app/modules/your_module_name/enter_methods.py`
* Conditions: `app/modules/your_module_name/conditions.py`

This will allow the program to parse your schema and apply your custom enter methods and conditions.

4) Implement Custom Scheduled Tasks Using the TaskCreator (Optional)

This project includes a custom task scheduler called TaskCreator. To utilize this feature, you can pass the following parameters to the TaskCreator:

* `time`: When the task should be executed.
* `session`: The session for which the task should be applied.
* `current_state`: The current state name.

With the `TaskCreator`, you can easily schedule messages to be sent at specific times based on the parameters provided.

5) Configure Email Notifications (Optional)

The project is pre-configured to support email notifications. To enable this functionality, set up your email server configuration in the Django settings file, and define email-related actions within your FSM states and enter methods.

With these steps completed, you will have successfully customized the project for your own use case. Be sure to thoroughly test your implementation to ensure that your FSM tree operates as expected in both development and production environments.

### Running Tests and Linting Checks

1. Run tests: Use the command `docker compose exec app python manage.py test` to execute the test suite.
2. Perform linting checks: Utilize the command `docker compose exec app flake8` to run linting checks on your code.
