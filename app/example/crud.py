from http import HTTPStatus

from fastapi import HTTPException, APIRouter

from app.example.models import ExampleTable
from app.utils.base_crud import BaseAuthorize
from app.utils.cbv import cbv

example_crud_router = APIRouter()


@cbv(example_crud_router)
class ExampleCRUD(BaseAuthorize):
    @example_crud_router.get('/example/{example_id}')
    async def get_example(self, example_id: int):
        example_data = await self.session.get(ExampleTable, example_id)
        if not example_data:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        return example_data
