import os
import logging
from loguru import logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.auth import auth

app = FastAPI(title="Authorization")

SECRET_KEY = os.getenv("SECRET_KEY")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
)

app.include_router(auth)


@app.get("/")
async def service():
    return {"service": app.title}

