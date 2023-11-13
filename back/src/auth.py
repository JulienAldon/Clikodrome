import aiohttp
import pydantic
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse

from src.configuration import options
from src.identity import token

router = APIRouter(prefix='/api/auth')

@router.get('/azure')
async def start_auth():
    await token.refresh_keys()
    if token.configuration is None:
        raise HTTPException(status_code=503)
    # TODO: Use PKCE flow
    return RedirectResponse(
        f'{token.configuration.authorization_endpoint}'
        f'?client_id={options.client_id}'
        f'&client_secret={options.client_secret}'
        f'&redirect_uri={options.public_uri}/auth/redirect'
        f'&response_type=code&response_mode=query'
        f'&scope=openid+email'
        f'&state=123'
    )

class AccessToken(pydantic.BaseModel):
    access_token: str | None = None
    id_token: str | None = None
    error_description: str | None = None

@router.get('/redirect')
async def finalize_auth(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
    redirect_uri: str | None = None,
):
    if code is None:
        raise HTTPException(status_code=401, detail=error_description)
    await token.refresh_keys()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            token.configuration.token_endpoint,
            data={
                'client_id': options.client_id,
                'client_secret': options.client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': f'{options.public_uri}/auth/redirect',
                'scope': 'openid email',
            },
        ) as token_response:
            data = AccessToken.parse_raw(await token_response.read())
            if data.id_token is None:
                raise HTTPException(status_code=401, detail=data.error_description)
            response = RedirectResponse(options.frontend_uri)
            print(data.id_token)
            claims = await token.validate(data.id_token)
            response.set_cookie('token', data.id_token)
            response.set_cookie('user', claims['email'])
            response.set_cookie('role', claims['intra-role'])
            return response

@router.post('/token')
async def finalize_token(
    code: str | None = None,
    state: str | None = None,
    redirect_uri: str | None = None,
    error_description: str | None = None,
    error: str | None = None,
):
    print(code)
    if code is None:
        raise HTTPException(status_code=401, detail=error_description)
    await token.refresh_keys()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            token.configuration.token_endpoint,
            data={
                'client_id': options.client_id,
                'client_secret': options.client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': f'{options.desktop_redirect}',
                'scope': 'openid email',
            },
        ) as token_response:
            data = AccessToken.parse_raw(await token_response.read())
            if data.id_token is None:
                raise HTTPException(status_code=401, detail=data.error_description)
            claims = await token.validate(data.id_token)
            return {
                'token': data.id_token,
                'user': claims['email'],
                'role': claims['intra-role']
            }