from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import auth

app = FastAPI(title="Authorization")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(auth)

@app.get("/")
async def service():
    return {"service": app.title}



