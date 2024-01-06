from fastapi import FastAPI

app = FastAPI()

@app.get("/id/{id}")
async def show_id(id: int, qp: int | None = None):
    resultado = {"id": id}
    if qp:
        resultado.update({"qp": qp})
    return resultado