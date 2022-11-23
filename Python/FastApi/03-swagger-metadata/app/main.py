from typing import Union

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    docs_url = "/api/v1/docs",
    redoc_url = "/api/v1/redocs",
    title = "My API",
    description = "My super simple api",
    version = "1.0",
    openapi_url = "/api/v1/openapi.json"
)


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None



@app.get('/')
async def get_root():
    return {'message': 'Hello World'}


@app.get('/items/{item_id}', tags=['Items'])
async def get_items(item_id):
    return {'item': item_id}


@app.post('/items/{item_id}', tags=['Items'])
async def new_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results