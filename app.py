# -*- coding: utf-8 -*-
'''
    Simple API
'''
import base64
import json
from time import time
import requests

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware


_ORIGINS = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:8000",
        "http://localhost:4200",
    ]



app = FastAPI(title='API Model')
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.middleware('http')
async def remove_file_before_leave(request: Request, call_next):
  start_time = time()
  response = await call_next(request)
  process_time = time()
  response.headers['X-Process-Time'] = str(process_time - start_time)
  return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', tags=['Version 1'])
async def get_main():
  response = requests.get('https://randomuser.me/api/')
  return response.json()

if __name__ == '__main__':
 uvicorn.run(app, host='0.0.0.0', port=8000, debug=True)