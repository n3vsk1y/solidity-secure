import sys
import logging
from loguru import logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())

def logger_formater(record):
    record["extra"]["location"] = f"{record['name']}:{record['function']}:{record['line']}"
    return True

logger.remove()
logger.add(
    sys.stdout,
    format="<italic><cyan>{time:DD-MM HH:mm:ss}</cyan></italic> | "
           "<level>{level: <8}</level> | "
           "<cyan>{extra[location]: <45}</cyan> | "
           "<level>{message}</level>",
    filter=logger_formater
)

logging.basicConfig(handlers=[InterceptHandler()], level=0)


app = FastAPI(title="Analyze Service")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.get("/")
async def service():
    return {"service": app.title}


@app.get("/ping")
async def ping():
    return {"ping": "pong"}


if __name__ == "__main__":
    logger.debug(f"{app.title} запущен на http://0.0.0.0:8000")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=None,
    )