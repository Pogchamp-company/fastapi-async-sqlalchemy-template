# ProjectName

* [Description](#description)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Install & Run project](#install--run-project)
* [Contributing](#contributing)
    * [Code Style](#code-style)
    * [Branch naming](#branch-naming)
* [Environment variables](#environment-variables)
* [Project structure](#project-structure)

## Description
Your project description


## Getting Started

### Prerequisites

1. [Python3](https://www.python.org)
2. [PostgreSQL](https://www.postgresql.org)

### Install & Run project

1. Clone repo

```shell
git clone Your project url
```

2. Create Python Virtual Environment
3. Install requirements

```shell
pip install -r requirements/requirements.txt
```

4. Create PostgreSQL database
5. Make .env file

```shell
touch .env
```

6. Set [env variables](#environment-variables)
7. Migrate database

```shell
# cd src
alembic upgrade head
```

8. Run project

```shell
source venv/bin/activate
python manage.py serve --workers 1
```

## Run tests

1. Install tests requirements
```shell
pip install -r requirements/test_requirements.txt
```

2. Create db with prefix "test_"
3. Run pytest
```shell
source venv/bin/activate
pytest
```

### Tests coverage
```shell
pytest --cov=app --cov-report=html --cov-config=.coveragerc tests/ 
```


## Contributing

### Code style

[pep8](https://www.python.org/dev/peps/pep-0008/)
[FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)

### Branch naming

{username}/{task_short_description}

## Environment variables

| Variable             |  Description   |                       Default                        |
|----------------------|:--------------:|:----------------------------------------------------:|
| DATABASE_URI         | PostgreSQL URI | postgresql+asyncpg://postgres@localhost:5432/db_name |
| BACKEND_CORS_ORIGINS |    Frontend    |                          []                          | 
| HOST                 |       -        |                      127.0.0.1                       | 
| PORT                 |       -        |                         8000                         | 
| DEBUG                |       -        |                        False                         | 

## Project structure
Project structure id described [here](app/README.md)
