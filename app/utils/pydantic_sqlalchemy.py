# Based on https://github.com/tiangolo/pydantic-sqlalchemy


from typing import Container, Optional, Type, Any

from pydantic import BaseConfig, BaseModel, create_model
from sqlalchemy import Column
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.properties import ColumnProperty

from app.database import BaseModel as BaseSqlalchemyModel


class _ResultModel(BaseModel):
    @property
    def default_obj(self) -> BaseSqlalchemyModel:
        ...


class _OrmConfig(BaseConfig):
    orm_mode = True


class _SqlalchemyToPydantic:
    def __init__(self, db_model: Type[BaseSqlalchemyModel], *, config: Type = _OrmConfig, include: Container[str] = ()):
        self.db_model = db_model
        self.config = config
        self.include = include

    @staticmethod
    def get_python_type_from_sqla_column(column: Column) -> type:
        python_type: Optional[type] = None
        if hasattr(column.type, "impl"):
            if hasattr(column.type.impl, "python_type"):
                python_type = column.type.impl.python_type
        elif hasattr(column.type, "python_type"):
            python_type = column.type.python_type
        assert python_type, f"Could not infer python_type for {column}"
        return python_type

    @staticmethod
    def get_default_value_from_sqla_column(column: Column) -> Any:
        try:
            default = column.default.arg
        except AttributeError:
            default = None
        if callable(default):
            try:
                default = default()
            except:
                default = None
        if column.default is None and not column.nullable:
            default = ...
        return default

    def validate_model_attr(self, attr: Column | ColumnProperty | Any) -> bool:
        if not (isinstance(attr, ColumnProperty) and attr.columns):
            return False
        return not (attr.key not in self.include and self.include)

    def __call__(self) -> Type[_ResultModel]:
        mapper = inspect(self.db_model)
        fields = {}
        for attr in mapper.attrs:
            if not self.validate_model_attr(attr):
                continue

            column = attr.columns[0]
            python_type: type = self.get_python_type_from_sqla_column(column)

            fields[attr.key] = (python_type, self.get_default_value_from_sqla_column(column))

        pydantic_model = create_model(
            self.db_model.__name__, __config__=self.config, **fields,
        )

        pydantic_model.default_obj = property(lambda _: self.db_model())
        return pydantic_model


def sqlalchemy_to_pydantic(
        db_model: Type[BaseSqlalchemyModel], *, config: Type[BaseConfig] = _OrmConfig, include: Container[str] = (),
) -> Type[_ResultModel]:
    """
    Transform sqlalchemy model to pydantic model
    :param db_model: Sqlalchemy model
    :param (optional) config: Use it, if you need custom config to pydantic model. By default, config enable orm_mode
    :param (optional) include: If you only need specific fields of the model, use this parameter.
    By default, all fields are included
    :return: pydantic.BaseModel
    """
    return _SqlalchemyToPydantic(db_model, config=config, include=include)()
