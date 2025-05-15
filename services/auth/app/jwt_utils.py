import os
import jwt
from datetime import datetime
from datetime import timedelta


API_SECRET_KEY = os.getenv('API_SECRET_KEY')
API_ALGORITHM = os.getenv('API_ALGORITHM')
API_ACCESS_TOKEN_EXPIRE_MINUTES = 30
API_REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30  # 30 days


async def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt

def create_token(user_id: str, email: str, expires_delta: timedelta = None) -> str:
    payload = {
        "sub": user_id,  # "sub" (subject) — стандартное поле для ID пользователя
        "email": email,
        "exp": datetime.utcnow() + (expires_delta or timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)),
    }
    return jwt.encode(payload, API_SECRET_KEY, algorithm=API_ALGORITHM)


async def create_refresh_token(email: str) -> str:
    expires = timedelta(minutes=API_REFRESH_TOKEN_EXPIRE_MINUTES)
    return await create_access_token(data={'sub': email}, expires_delta=expires)


async def create_token(email: str) -> str:
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={'sub': email}, expires_delta=access_token_expires)
    return access_token


async def decode_token(token: str) -> dict:
    return jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])

