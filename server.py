import os
import sys
import json
import uvicorn
import logging

from importlib import import_module

from fastapi import FastAPI, Request, Response, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from lib.config import Config
from lib.document_handler import DocumentHandler

## Load the configuration and set some defaults
configPath = 'config.json'
with open(configPath, 'r', encoding='UTF-8') as config_file:
    config = Config(json.loads(config_file.read()))
config.port = os.getenv('PORT') or config.port or 7777
config.host = os.getenv('HOST') or config.host or 'localhost'


## Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


## build the store from the config on-demand - so that we don't load it
## for statics
if not config.storage:
    config.storage = Config({'type': 'file'})
if not config.storage.type:
    config.storage.type = 'file'

store = import_module('lib.document_stores.' + config.storage.type)
preferredStore = store.Store(config.storage)


## Compress the static javascript assets
#
#


## Send the static documents into the preferred store, skipping expirations
for name in config.documents.dict:
    path = config.documents.dict[name]
    with open(path, 'r', encoding='UTF-8') as data: data = data.read()
    logger.info('loading static document', f"name: {name}, path: {path}")

    if data:
        preferredStore.set(name, data, True)
    else:
        logger.warn('failed to load static document', f"name: {name}, path: {path}")


## Pick up a key generator
pwOptions = config.keyGenerator
pwOptions.type = pwOptions.type or 'random'
generator = import_module(f'lib.key_generators.' + pwOptions.type)
keyGenerator = generator.gen()


## Configure the document handler
documentHandler = DocumentHandler(Config({
    'store': preferredStore,
    'maxLength': config.maxLength,
    'keyLength': config.keyLength,
    'keyGenerator': keyGenerator
}))


app = FastAPI()
app.router.redirect_slashes = False

templates = Jinja2Templates(directory="static")

## first look at API calls
## get raw documents - support getting with extension
@app.get("/raw/{id}", response_class=PlainTextResponse)
async def raw_get(request: Request, response: Response):
    return documentHandler.handleRawGet(request, response, config)

@app.head("/raw/{id}")
async def raw_head(request: Request, response: Response):
    return documentHandler.handleRawGet(request, response, config)

## add documents
@app.post("/documents")
async def docs(request: Request, response: Response):
    buffer = await request.body()
    return documentHandler.handlePost(request, response, buffer)

## get documents
@app.get("/documents/{id}")
async def docs_get(request: Request, response: Response):
    return documentHandler.handleGet(request, response, config)

@app.head("/documents/{id}")
async def docs_head(request: Request, response: Response):
    return documentHandler.handleGet(request, response, config)


## And match index
@app.get("/", response_class=HTMLResponse)
@app.get("/{id}", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})


## Otherwise, try to match static files
app.mount("/static/", StaticFiles(directory="static", html=False), name="static")


logger.info('listening on ' + config.host + ':' + str(config.port))

if __name__ == '__main__':
    uvicorn.run("server:app", host=config.host, port=config.port, workers=4)