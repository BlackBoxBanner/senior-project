from fastapi import FastAPI, File
from fastapi.responses import JSONResponse
from typing import Annotated
from module.ui_rules import ui_rules

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/603010")
async def upload_image(image: Annotated[bytes, File()]):
    ui = ui_rules.UIRulesModule(image)
    result = ui.check_60_30_10_rule()
    return JSONResponse(content=result)
