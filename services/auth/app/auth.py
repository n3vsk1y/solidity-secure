from fastapi import APIRouter, HTTPException
from loguru import logger
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuthError

from app.db import valid_email_from_db
from app.oauth import oauth
from app.jwt_utils import create_token, verify_token
from app.error import CredentialsError

auth = APIRouter(tags=['Authentication'])


@auth.get('/')
async def public(request: Request):
    # user = request.session.get('user')
    # if user:
    #     name = user.get('name')
    #     return HTMLResponse(f'<p>Hello {name}!</p><a href='/logout'>Logout</a>')
    # return HTMLResponse('<body><a href='/auth/login'>Log In</a></body>')

    request_info = {
        'user': request.session.get('user'),
        'method': request.method,
        'url': str(request.url),
        'headers': dict(request.headers),
        'query_params': dict(request.query_params),
        'path_params': dict(request.path_params),
        'cookies': dict(request.cookies),
        'client': {'host': request.client.host, 'port': request.client.port} if request.client else None,
    }
    return JSONResponse(request_info)


@auth.get('/login')
async def login(request: Request):
    redirect_uri = 'http://localhost/api/auth/callback'
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth.get('/callback')
async def callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
    except OAuthError as e:
        return HTTPException(status_code=401, detail=f'OAuthError: {str(e)}')
    except Exception as e:
        return HTTPException(status_code=401, detail=f'error: {str(e)}')

    if not valid_email_from_db(user['email']):
        return HTTPException(status_code=403, detail='Email not allowed')

    access_token = await create_token('access', user['sub'], user['email'], user['name'], user['picture'])
    refresh_token = await create_token('refresh', user['sub'], user['email'], user['name'], user['picture'])

    response = RedirectResponse(url=f'http://localhost/?access_token={access_token}')
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='None',
        max_age=30 * 24 * 60 * 60,
        path='/',
    )

    return response


@auth.get('/check')
async def check(request: Request):
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise HTTPException(status_code=401, detail='Not authenticated')

    try:
        payload = await verify_token(refresh_token)
        return {
            "user_id": payload["sub"],
            "email": payload["email"],
            "name": payload.get("name"),
            "picture": payload.get("picture"),
        }
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid or expired token')


# @auth.post('/refresh')
# async def refresh(request: Request):
#     try:
#         data = await request.json()
#         refresh_token = data.get('refresh_token')
#         if not refresh_token:
#             raise CredentialsError('Refresh token is missing')

#         payload = decode_token(refresh_token, config['JWT_SECRET_KEY'])
#         if not payload:
#             raise CredentialsError('Invalid refresh token')

#         user_id = payload.get('sub')
#         email = payload.get('email')

#         access_token = create_token(user_id, email)
#         refresh_token = create_refresh_token(user_id, email)

#         return JSONResponse(
#             status_code=200,
#             content={
#                 'access_token': access_token,
#                 'refresh_token': refresh_token,
#                 'expires_in': 3600,
#                 'token_type': 'Bearer',
#                 'scope': 'openid email profile'
#             }
#         )
#     except CredentialsError as e:
#         return JSONResponse(status_code=401, content={'error': str(e)})
#     except Exception as e:
#         return JSONResponse(status_code=500, content={'error': str(e)})
