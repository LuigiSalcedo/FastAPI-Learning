from fastapi import FastAPI, Query, Path, Body
from typing import Annotated, Any

app = FastAPI()

# greater than -> mayor que
@app.get("/users/{id}", summary="obtener usuario")
async def get_user(id: Annotated[int, Path(gt=0, example=123, description="id del usuario")], 
                   name: Annotated[str | None, Query(min_length=4, max_length=8, example="Yurleis")] = None):
    """
    Este endpoint es para "consultar" un usuario por id y opcionalmente por el nombre

    - **id**: es un path param que es entero mayor que 0
    - **name**: es un query param con longitud mayor o igual 4 o menor o igual a 8
    """
    result = {"id": id}
    if name:
        result.update({"name": name})

    return result

@app.post("/imprimir", summary="imprimir en el servidor un objeto")
async def server_print(object: Annotated[dict[str, Any], Body(example={"id": 1, "name": "Yurleis"})]):
    """
    Imprimir un objeto en el servidor
    """
    print(object)