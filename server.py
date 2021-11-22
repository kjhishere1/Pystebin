import os
import sys
import json
import logging

import js2py

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

## Load the configuration and set some defaults
configPath = 'config.json' if (len(sys.argv) <= 2) else sys.argv[2]
config = json.loads(open(configPath, 'r', encoding='utf8').read())
config['port'] = os.getenv('PORT') or config['port'] or 7777
config['host'] = os.getenv('HOST') or config['host'] or 'localhost'


## Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_hander = logging.StreamHandler()
stream_hander.setFormatter(formatter)
logger.addHandler(stream_hander)


## build the store from the config on-demand - so that we don't load it
## for statics
#
#


## Compress the static javascript assets
#
#


## Send the static documents into the preferred store, skipping expirations
#
#


## Pick up a key generator
#
#


## Configure the document handler
#
#


app = FastAPI()

## first look at API calls
## get raw documents - support getting with extension
@app.get("/raw/{doc_id}")
async def raw_get(doc_id: str):
    return doc_id

@app.head("/raw/{doc_id}")
async def raw_head(doc_id: str):
    return doc_id


## add documents
@app.post("/documents")
async def docs():
    return


## get documents
@app.get("/documents/{doc_id}")
async def docs_get(doc_id: str):
    return doc_id

@app.head("/documents/{doc_id}")
async def docs_head(doc_id: str):
    return doc_id


## And match index
app.mount("/", StaticFiles(directory="static", html=True), name="static")