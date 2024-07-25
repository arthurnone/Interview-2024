# Flask Web Project

This is a Flask web project that includes a Flask application, unit tests, and configurations for Docker, Nginx.

## SUMMARY

This project, developed using Flask, provides CRUD (Create, Read, Update, Delete) operations for the "recipes" table in a MySQL database. It employs a RESTful architecture for designing the API. Additionally, the project includes a logging system to record API errors and database operation errors. A unit testing module has been added, with test cases developed for each endpoint. After testing, a coverage report is generated.

The project can be started directly using Python or deployed using Docker. Nginx configuration is provided to act as a reverse proxy for my server. 

Due to time constraints, caching and authorization modules were not added. Including these modules would enhance the project, making it a complete solution capable of supporting certain medium-sized projects.

## Project Structure

```
.
├── app
│ ├── init.py
│ ├── db.py
│ ├── logger.py
│ ├── routes.py
│ ├── models
│ │    └── recipe.py
│ └── api
│ │    └── recipes.py
├── tests
│ └── test_api.py
├── mysql_db
│ ├── create.sql
│ └── docker-compose.yml
├── config.py
├── wsgi.py
├── test_runner.py
├── test_db.py
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── build.sh
├── start.sh
└── requirements.txt
```

- `app/`: Contains the Flask application code.
  - `init.py`: Creating and configuring a Flask application
  - `db.py`: MySQL database configuration and initialization (singleton pattern)
  - `logger.py`: Basic logging configuration
  - `routes.py`: Flask routing configuration
  - `models/recipe.py`: Recipe model operations (CRUD operations on the database)
  - `api/recipes.py`: API handlers for recipe and recipes
- `tests/`: Contains the unit test code.
  - `tests/test_api.py`: Unit test cases for all API endpoints.
- `mysql_db/`: Directory for test database data and configuration
  - `mysql_db/create.sql`: This is the default SQL script provided for interview questions.
  - `mysql_db/docker-compose.yml`: Configuration file for test-mysql Docker Compose.
- `config.py`: Flask project configuration file.
- `wsgi.py`: Flask app WSGI entry file.
- `test_runner.py`: Unit tests and coverage test startup script.
- `test_db.py`: Script to refresh the test database.
- `Dockerfile`: Configuration file for Docker.
- `docker-compose.yml`: Configuration file for Docker Compose.
- `nginx.conf`: Configuration file for Nginx.
- `build.sh`: Script to initialize and build Docker image.
- `start.sh`: Script to start Flask using Gunicorn.
- `requirements.txt`: Python dependencies.

### Prerequisites

- Python 3.12.x
- MySQL 8.0.x
- Docker
- Docker Compose

### Installation

1. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Application

#### Locally

1. Run the Flask application:

   ```sh
   python wsgi.py
   ```

2. Access the application at `http://127.0.0.1:8088`.

#### Using Docker

1. Build the Docker image:

   ```sh
   bash build.sh
   ```

2. Run the Docker container:

   ```sh
   docker-compose up -d
   ```

3. Access the application at `http://127.0.0.1:8088`.

### Running Tests

1. Run the tests using pytest:
   ```sh
   python test_runner.py
   ```
