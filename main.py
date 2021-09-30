import os, sys

import uvicorn
from fastapi import FastAPI, Request, Body, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from contract.contract import registered_contract, w3

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/metamask", response_class=HTMLResponse)
async def conn_metamask(request: Request):
    return templates.TemplateResponse("connectiong.html", {"request": request})


@app.get("/state")
async def get_state():
    state = "state"
    state_func = registered_contract.functions[state]
    return state_func().call()


@app.post("/state")
async def change_state():
    registered_contract.functions.changeState(2).transact()
    return registered_contract.functions.state().call()


@app.post("/register")
async def register_account():
    print(registered_contract.functions.state().call())
    registered_contract.functions.register(w3.eth.accounts[2]).transact({"from": w3.eth.coinbase})
    return 200
    # return registered_contract.all_functions()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)