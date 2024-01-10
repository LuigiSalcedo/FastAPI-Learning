from fastapi import FastAPI, Query, Path, Header, Body
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

# Endpoint: Funciones que responden a una solicitud en base a un ruta
@app.get("/ping")
async def ping():
    return "pong"

# Path Param: Variable que viene por la URL como parte de la ruta
@app.get("/saludar/{nombre}")
async def saludar(nombre:str):
    return f"¡Hola {nombre}!"

# Query Param: Variable que es una query
@app.get("/saludar")
async def saludar_query(nombre:str, edad:Annotated[int | None, Query(alias="edad-p")] = None):
    mensaje = f"¡Hola {nombre}!"
    if edad: # Verifica que edad no es None
        mensaje = mensaje + f" Tienes {edad} años"
    return mensaje

@app.get("/multisaludo")
async def saludar_multiple(nombres: Annotated[list[str], Query()]):
    mensaje = ""
    for nombre in nombres: 
        mensaje = mensaje + f"Un saludo para: {nombre}, "
    return mensaje

# Definir una semáticas
@app.get("/verificar-nombre/{nombre}")
async def verificar_nombre(nombre: Annotated[str, Path(min_length=4, max_length=10)]):
    return {"nombre": nombre, "valido": True} # Diccionario

@app.get("/verificar-nombre-query")
async def verificar_nombre_query(nombres: Annotated[list[str], Query()]):
    response = {}
    for nombre in nombres:
        if len(nombre) == 5:
            response.update({nombre: False})
        else:
            response.update({nombre: True})
    return response

@app.get("/verificar-cabezera")
async def verificar_cabecera(token: Annotated[str, Header(alias="Token-Especial")]):
    if token == 'FastYurleis':
        return "Usted ha accedido correctamente"
    return "Acceso denegado"

class Modelo(BaseModel):
    id:int
    nombre:str

# Enviar un modelo embebido
@app.post("/enviar-modelo")
async def enviar_modelo(modelo: Annotated[Modelo, Body()]):
    return {"modelo": modelo}

# Retornar un modelo
@app.get("/recibir-modelo", response_model=Modelo)
async def recibir_modelo():
    return Modelo(id=1, nombre="Jane Doe")

# Sacar un modelo embebido
@app.post("/modelo-embebido", response_model=Modelo)
async def modelo_embebido(modelo: Annotated[Modelo, Body(embed=True)]):
    return modelo