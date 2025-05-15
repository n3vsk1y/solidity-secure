from fastapi import APIRouter
from loguru import logger
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuthError

from app.db import valid_email_from_db
from app.oauth import oauth
from app.jwt_utils import create_token, create_refresh_token, decode_token
from app.error import CredentialsError

auth = APIRouter(tags=['Authentication'])


@auth.get('/')
async def public(request: Request):
    # user = request.session.get('user')
    # if user:
    #     name = user.get('name')
    #     return HTMLResponse(f'<p>Hello {name}!</p><a href="/logout">Logout</a>')
    # return HTMLResponse('<body><a href="/auth/login">Log In</a></body>')

    request_info = {
        'user': request.session.get('user'),
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "path_params": dict(request.path_params),
        "cookies": dict(request.cookies),
        "client": {"host": request.client.host, "port": request.client.port} if request.client else None,
    }
    return JSONResponse(request_info)


@auth.get('/login')
async def login(request: Request):
    redirect_uri = "http://localhost/api/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth.get('/callback')
async def callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = await oauth.google.parse_id_token(request, token=token)
        return JSONResponse(status_code=200, content={"user": user})
    except OAuthError as e:
        return JSONResponse(status_code=401, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=401, content={"error": str(e)})

    if not valid_email_from_db(user['email']):
        return JSONResponse(status_code=403, content={"error": "Email not allowed"})

    access_token = create_token(user['sub'], user['email'])
    refresh_token = create_refresh_token(user['sub'], user['email'])

    return JSONResponse(
        status_code=200,
        content={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': 3600,
            'token_type': 'Bearer',
            'scope': 'openid email profile'
        }
    )


# @auth.post('/refresh')
# async def refresh(request: Request):
#     try:
#         data = await request.json()
#         refresh_token = data.get('refresh_token')
#         if not refresh_token:
#             raise CredentialsError("Refresh token is missing")

#         payload = decode_token(refresh_token, config['JWT_SECRET_KEY'])
#         if not payload:
#             raise CredentialsError("Invalid refresh token")

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
#         return JSONResponse(status_code=401, content={"error": str(e)})
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})












