from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from db import valid_email_from_db, is_token_blacklisted
from error import CredentialsError
from jwt_utils import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


async def get_current_user_email(token: str = Depends(oauth2_scheme)):
    if await is_token_blacklisted(token):
        raise CredentialsError("Token blacklisted")
    try:
        payload = await decode_token(token)
        email: str = payload.get('sub')
        if email is None:
            raise CredentialsError("Credentials exception")
    except Exception as e:
        raise CredentialsError(e.message)

    if await valid_email_from_db(email):
        return email

    raise CredentialsError("Bad credentials")

async def get_current_user_token(token: str = Depends(oauth2_scheme)):
    _ = await get_current_user_email(token)
    return token
