import os
import jwt
import datetime


API_SECRET_KEY = os.getenv('API_SECRET_KEY')
API_ALGORITHM = os.getenv('API_ALGORITHM')
API_ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('API_ACCESS_TOKEN_EXPIRE_MINUTES')
API_REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv('API_REFRESH_TOKEN_EXPIRE_MINUTES')


async def create_token(type: str, user_id: str, email: str, name: str, picture: str) -> str:
    payload = {
        'sub': user_id,
        'email': email,
        'name': name,
        'picture': picture,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(int(API_ACCESS_TOKEN_EXPIRE_MINUTES if type == 'access' else API_REFRESH_TOKEN_EXPIRE_MINUTES)),
    }
    return jwt.encode(payload, API_SECRET_KEY, algorithm=API_ALGORITHM)


async def verify_token(token: str):
    try:
        return jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')