# Table of Contents:

- About
- Requirements
- Setup
- Canvas


## About

It is a predefined microservice structure with basic configuration. So, We can use this template to create new microservices instead of starting from the scratch

## Requirements

- Python 3.9
- Redis rejson 6.0.9
- MySQL 5.7.32
- RabbitMQ
- Works on Linux, Windows


## Setup

1. Clone the repository
2. Create a virtual environment
3. Install all the dependencies from the requirements.txt file using the command `pip install -r requirements.txt`
4. Set environment variables
5. Execute command `pytest` to test the service
5. Run the `run.py` file to start the service


## Canvas

### Capabilities:
- Add person
- Get person
- Update person
- Delete person


### Service APIS:

- #### command:
    - addPerson()
    - getPerson()
    - updatePerson()
    - deletePerson()

- #### Queries:
    - None

- #### Event Published:
    - None


### Dependencies:
- #### Invokes
    - None

- #### Subscribed to
    - None


### addPerson()
- #### API contract:
  - Swagger link

- #### Flow:

  Step 1: Validate the request header and payload
  Step 2: Add a person in SQL person table\
  Step 3: If a person already exists then raise exception\
  Step 4: Add a person object into the Redis\
  Step 5: Return a person object in API response


### getPerson()
- #### API contract:
  - Swagger link

- #### Flow:

    Step 1: Get person object from the Redis\
    Step 2: If not found in redis then got to step 3 else step 6\
    Step 3: Get person from SQL person table\
    Step 4: If person not found in SQL then raise exception\
    Step 5: Add person in redis\
    Step 6: Return a person object in API response

### updatePerson()
- #### API contract:
  - Swagger link

- #### Flow:

    Step 1: Update a person in SQL person table\
    Step 2: If a person not found then raise exception\
    Step 3: Update a person object in Redis\
    Step 4: If Redis object not found then got to step 5 else step 6\
    Step 5: Get a person from SQL person table\
    Step 6: Add a person in redis\
    Step 7: Return a person object in API response

### deletePerson()
- #### API contract:
  - Swagger link

- #### Flow:

    Step 1: Delete a person from the SQL person table\
    Step 2: If a person not found then raise exception\
    Step 3: Delete a person object from the Redis\
    Step 4: Return success response

## Pre commit hooks

- Install pre-commit hooks

  ```bash
  $ pip install -r requirements_dev.txt
  $ pre-commit install
  ```
