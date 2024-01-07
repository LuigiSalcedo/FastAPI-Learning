from fastapi import FastAPI, Query, HTTPException, Path, Request
from fastapi.responses import JSONResponse
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    name:str
    price:float

database:dict[str, Product] = {
    "X12": Product(name="Agua", price=1000),
    "ABC": Product(name="Gaseosa", price=2000)
}

class ProductNotFoundException(Exception):
    def __init__(self, id:str):
        self.id = id

@app.exception_handler(ProductNotFoundException)
async def product_not_found_handler(req: Request, exception: ProductNotFoundException):
    return JSONResponse(status_code=404, content={
        "path": req.url.path,
        "method": req.method,
        "detail": f"There is not a product with {exception.id} id"
    })

@app.get("/test-error")
async def test_error(q: Annotated[int, Query(gt=0, le=10)]):
    if q == 5:
        raise HTTPException(status_code=400, detail="number 5 is not accepted")
    return {"number": q}

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: Annotated[str, Path(min_length=3)]):
    product = database.get(product_id)
    if product is None:
        raise ProductNotFoundException(id=product_id)
    return product
