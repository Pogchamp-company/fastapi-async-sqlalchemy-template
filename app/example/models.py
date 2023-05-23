from sqlalchemy import Column, Integer

from app.database import BaseModel


class TestTable(BaseModel):
    test_field = Column(Integer, primary_key=True, autoincrement=False)
