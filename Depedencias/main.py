from fastapi import FastAPI, Depends, Query, HTTPException
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

class QueryDependencies(BaseModel):
    param1:int
    param2:int | None = None

def parse_depedencies(param1:int, param2:int | None = None):
    if param1 == 5 or param2 == 5:
        raise HTTPException(status_code=400, detail="5 is not allowed")
    
    dependencies = QueryDependencies(param1=param1)

    if param2:
        dependencies.param2 = param2
    
    return dependencies

@app.get("/dependencies")
async def get_dependencies(dependencies: Annotated[QueryDependencies, Depends(parse_depedencies)]):
    return dependencies