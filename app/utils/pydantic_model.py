from pydantic import BaseModel


class BasePydanticModel(BaseModel):
    def populate_obj(self, obj) -> None:
        """
        Fill obj attributes from pydantic model
        :param obj: object with attributes (Most often SQLAlchemy model)
        """

        for field_name, form_value in vars(self).items():
            if not hasattr(obj, field_name):
                continue

            # The value is not a nested pydantic model
            if not hasattr(form_value, 'populate_obj'):
                setattr(obj, field_name, form_value)
                continue

            # If the object is a nested object (e.g. relationship), often we want an empty object instead of None
            obj_value = getattr(obj, field_name)
            if obj_value is None and hasattr(form_value, 'default_obj'):
                obj_value = form_value.default_obj
                setattr(obj, field_name, obj_value)

            form_value.populate_obj(obj_value)

    class Config:
        orm_mode = True
