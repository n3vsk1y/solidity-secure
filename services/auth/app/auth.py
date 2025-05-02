import os
import uvicorn
from fastapi import APIRouter
from fastapi import Request

from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError

from app.error import EnvVariablesError

auth = APIRouter(tags=['Auther'])

# OAuth settings
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise EnvVariablesError('Missing env variables')

@auth.get('/')
async def test():
    return {"auther": "внутри роута"}

@auth.get('/login')
async def test():
    return {"login": "внутри роута"}

# Set up OAuth
# config_data = {
#     'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 
#     'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET
# }
# starlette_config = Config(environ=config_data)
# oauth = OAuth(starlette_config)
# oauth.register(
#     name='google',
#     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={'scope': 'openid email profile'},
# )



# @auth.get('/')
# def public(request: Request):
#     user = request.session.get('user')
#     if user:
#         name = user.get('name')
#         return HTMLResponse(f'<p>Hello {name}!</p><a href=/logout>Logout</a>')
#     return HTMLResponse('<a href=/login>Login</a>')


# @auth.route('/logout')
# async def logout(request: Request):
#     request.session.pop('user', None)
#     return RedirectResponse(url='/')


# @auth.route('/login')
# async def login(request: Request):
#     redirect_uri = request.url_for('auth')  # This creates the url for our /auth endpoint
#     return await oauth.google.authorize_redirect(request, redirect_uri)


# @auth.route('/auth')
# async def auth(request: Request):
#     try:
#         access_token = await oauth.google.authorize_access_token(request)
#     except OAuthError:
#         return RedirectResponse(url='/')
#     user_data = await oauth.google.parse_id_token(request, access_token)
#     request.session['user'] = dict(user_data)
#     return RedirectResponse(url='/')

