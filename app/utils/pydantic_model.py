from pydantic import BaseModel


class BasePydanticModel(BaseModel):
    def populate_obj(self, obj):
        for var, value in vars(self).items():
            if hasattr(obj, var):
                if hasattr(value, 'populate_obj'):
                    obj_value = getattr(obj, var)
                    if obj_value is None and hasattr(value, 'default_obj'):
                        obj_value = value.default_obj
                        setattr(obj, var, obj_value)
                    value.populate_obj(obj_value)
                else:
                    setattr(obj, var, value)

    class Config:
        orm_mode = True
