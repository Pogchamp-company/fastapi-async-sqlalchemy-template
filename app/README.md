# About project structure

## Project structure

### models.py

All models present in the project must be imported here.

### core/config.py

All project settings are located here.

### utils

#### base_cbv.py

This class contains the fields session (sqlalchemy.ext.asyncio.AsyncSession) and logger (logging.Logger).
All Class-Based Views inherit from this class.

#### base_response_schemas.py

The most common standard server responses are described here.

#### cbv.py

Utility for generating routers from classes.

#### logging

Logging is done in JSON format, using the json_logging library.
The code for describing the fields that will be used for logging is located in **logs_formatter.py**.
The dependency for obtaining the project's default logger is located in **get_logger.py**.

#### pydantic

**pydantic_model.py** contains an extension of the standard BaseModel class that adds support for populating fields of objects from the model using the populate_obj method.
**pydantic_sqlalchemy.py** contains the function for generating a pydantic model from a sqlalchemy model.

## Application structure

├── app_name
│   ├── api
│   │   ├── \_\_init__.py
│   │   ├── v1.py
│   ├── crud.py
│   ├── models.py # Sqlalchemy models must contains here
│   ├── schemas.py # Pydantic models must contains here

Remember to connect your routers in `app.app.init_routers`

