import os, sys

import uvicorn
from fastapi import FastAPI, Request, Body, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from contract.contract import registered_contract

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/metamask", response_class=HTMLResponse)
async def conn_metamask(request: Request):
    return templates.TemplateResponse("connectiong.html", {"request": request})


@app.post("/register")
async def register_account():
    a = registered_contract.functions.register("0x7A0F1Ce6c65Ba1468CFf871A4A1f308Bf99FE423").transact()
    return a
    # return registered_contract.all_functions()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)