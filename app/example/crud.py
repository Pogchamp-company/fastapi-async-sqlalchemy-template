from http import HTTPStatus

from fastapi import HTTPException, APIRouter

from app.example.models import ExampleTable
from app.utils.base_cbv import BaseCBV
from app.utils.cbv import cbv

example_crud_router = APIRouter()


@cbv(example_crud_router)
class ExampleCRUD(BaseCBV):
    @example_crud_router.get('/example/{example_id}')
    async def read(self, example_id: int):
        example_data = await self.session.get(ExampleTable, example_id)
        if not example_data:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        return example_data
