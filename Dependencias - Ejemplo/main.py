from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel, Field
from typing import Annotated

class ProductUpdate(BaseModel):
    name:str | None = Field(min_length=3, max_length=20, default=None)
    price:float | None = Field(ge=0, default=None)
    tax:float | None = Field(ge=0, default=None)


class Product(BaseModel):
    # Definimos un ID mayor que 0
    id:int = Field(gt=0) 

    # Nombre entre 3 y 20 caracteres
    name:str = Field(min_length=3, max_length=20) 

    # Un precio que debe ser mayor o igual a 0
    price:float = Field(ge=0) 

    # Impuesto mayor o iguales a 0, por defecto, del 19%
    tax:float = Field(ge=0, default=0.19) 

db:dict[int, Product] = {
    1: Product(id=1, name="Botella de agua", price=1500), # Por defecto tendrá impuesto del 19%
    2: Product(id=2, name="Dulce", price=5000, tax=0.25),
    3: Product(id=3, name="Frutas", price=2000, tax=0.10)
}

app = FastAPI()

# Dependencia para buscar un producto en la base de datos
def search_product(product_id:int) -> Product:
    product = db.get(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    
    return product

# Convertir de Query Param a ProductUpdate
def get_update_data(
        name:str | None = None, 
        price:float | None = None, 
        tax:float | None = None) -> ProductUpdate:
    return ProductUpdate(name=name, price=price, tax=tax)


@app.get(
    "/product/{product_id}",
    response_model=Product, # Es buena práctica aclarar que modelo vamos a retornar
    status_code=200,
    summary="obtener un producto por id"
)
# También puedes usarlo de esta forma: product: Annotated[Product, Depends(search_product)]
async def get_product(product: Product = Depends(search_product)):
    return product

@app.patch(
    "/product/update/{product_id}",
    response_model=Product,
    status_code=200,
    summary="actualizar datos de un producto"
)
async def update_product(
    # Obtener el product por dependencia
    product: Product = Depends(search_product),
    # Obtener la información a actualizar por dependencia
    update_data: ProductUpdate = Depends(get_update_data)):
    # Verificamos si enviaron cada uno de los parametros y actualizamos
    if update_data.name:
        product.name = update_data.name
    
    if update_data.price:
        product.price = update_data.price
    
    if update_data.tax:
        product.tax = update_data.tax

    # Lo guardamos en la base de datos simulada
    db[product.id] = product
    return product

@app.post(
    "/product/save",
    response_model=None,
    status_code=201,
    summary="guardar datos de un producto"
)
async def save_product(product: Annotated[Product, Body()]):
    # Lo buscamos en la base de datos
    p = db.get(product.id)

    # Si existe lanzamos una exception
    if p:
        raise HTTPException(status_code=400, detail="product already registered")
    
    # De lo contrario lo guardamos en la base de datos
    db[product.id] = product