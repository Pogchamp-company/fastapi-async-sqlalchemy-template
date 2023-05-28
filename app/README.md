# About project structure

## Project structure

### models.py

All models present in the project must be imported here.

### core/config.py

All project settings are located here.

### utils

#### base_cbv.py

This class contains the fields session (sqlalchemy.ext.asyncio.AsyncSession) and logger (logging.Logger).<br>
All Class-Based Views inherit from this class.

#### base_response_schemas.py

The most common standard server responses are described here.

#### cbv.py

Utility for generating routers from classes.

#### logging

Logging is done in JSON format, using the json_logging library.<br>
The code for describing the fields that will be used for logging is located in **logs_formatter.py**.<br>
The dependency for obtaining the project's default logger is located in **get_logger.py**.

#### pydantic

**pydantic_model.py** contains an extension of the standard BaseModel class that adds support for populating fields of objects from the model using the populate_obj method. <br>
**pydantic_sqlalchemy.py** contains the function for generating a pydantic model from a sqlalchemy model.

## Application structure

├── app_name<br>
│   ├── api<br>
│   │   ├── \_\_init__.py<br>
│   │   ├── v1.py<br>
│   ├── crud.py<br>
│   ├── models.py # Sqlalchemy models must contains here<br>
│   ├── schemas.py # Pydantic models must contains here<br>

Remember to connect your routers in [app.app.init_routers](app.py#L70)

