import os, sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contract.contract import w3

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/metamask", response_class=HTMLResponse)
async def conn_metamask(request: Request):
    return templates.TemplateResponse("connectiong.html", {"request": request})


@app.get("/account")
async def get_account():
    return w3.eth.get_accounts()