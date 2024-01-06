from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated

# Definir nuestro primero modelo
# gt = mayor que
# ge = mayor o igual que
# lt = menor que
# le = menor o igual que
class Person(BaseModel):
    id:int = Field(gt=0, le=100, examples=[99], default=1)
    name:str = Field(min_length=3, examples=["Yurleis"], default="John Doe")
    age:int = Field(gt=0, examples=[19], default=18)

class Product(BaseModel):
    name:str
    price:float
    tax:float

class Shop(BaseModel):
    id:int
    name:str
    product:list[Product]

app = FastAPI()

@app.get("/person", 
         summary="obtener una persona cualquiera",
         response_model=Person,
         response_model_exclude_defaults=True)
async def get_person():
    p = Person(id=50, name="Yurleis", age=19)
    return p

@app.post("/person", summary="imprimir un person en el servidor")
async def server_print(person: Annotated[Person, Body()]):
    print(person)

@app.post("/shop")
async def server_print_shop(shop: Annotated[Shop, Body()]):
    print(shop)