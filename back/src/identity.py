import time
from typing import Any
from urllib.error import HTTPError

import aiohttp
from fastapi import Cookie, Depends, HTTPException, Header
from jose import jwt
import pydantic

from .configuration import options

class JSONWebKey(pydantic.BaseModel):
    alg: str | None = None
    kty: str
    use: str
    n: str
    e: str
    kid: str
    x5t: str
    x5c: list[str]

    def rsa_key(self) -> dict[str, str]:
        return {
            "kty": self.kty,
            "kid": self.kid,
            "use": self.use,
            "n": self.n,
            "e": self.e,
        }

class JSONWebKeySet(pydantic.BaseModel):
    keys: list[JSONWebKey]

class OpenIDConfiguration(pydantic.BaseModel):
    token_endpoint:         str
    authorization_endpoint: str
    jwks_uri:               str

class TokenVerifier:
    keys: dict[str, JSONWebKey]
    def __init__(self, origin: str, *, refresh_seconds: float=3600.0, **options: dict[str, Any]):
        self._origin       = origin
        self._refresh_rate = refresh_seconds
        self._last_update  = 0
        self._options      = options
        self.configuration = None
        self.keys          = {}

    async def fetch_keys(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self._origin}/v2.0/.well-known/openid-configuration') as response:
                self.configuration = OpenIDConfiguration.parse_raw(await response.read())
            if self.configuration is None:
                self.keys.clear()
                return
            async with session.get(self.configuration.jwks_uri) as response:
                for key in JSONWebKeySet.parse_raw(await response.read()).keys:
                    self.keys[key.kid] = key
            self._last_update = time.time()

    async def refresh_keys(self):
        now = time.time()
        if now - self._last_update > self._refresh_rate:
            await self.fetch_keys()

    async def validate(self, token: str, *, _has_retried: bool=False) -> dict[str, Any]:
        await self.refresh_keys()

        header = jwt.get_unverified_header(token)
        try:
            key = self.keys[header['kid']]
        except KeyError:
            if not _has_retried:
                await self.fetch_keys()
                return self.validate_token(token, _has_retried=True)
        try:
            claims = jwt.decode(token, key.rsa_key(), key.alg, **self._options)
        except Exception as e:
            raise HTTPException(status_code=401)
        if 'email' not in claims:
            raise HTTPException(status_code=401)
        is_pedago = any(g in options.pedago_authorized_groups for g in claims.get('roles', []))
        is_assistant = any(g in options.assistant_authorized_groups for g in claims.get('roles', []))
        if is_pedago:
            role = 'pedago'
        elif is_assistant:
            role = 'assistant'
        else:
            role = 'student'
        claims['intra-role'] = role
        return claims

    async def __call__(self, authorization: str | None = Header(default=None), token: str | None = Cookie(default=None)) -> dict[str, Any]:
        if token is not None:
            return await self.validate(token)
        if authorization is None:
            raise HTTPException(status_code=401)
        try:
            split_header = authorization.split(maxsplit=1)
            if split_header[0] != 'Bearer' and len(split_header) != 2:
                raise HTTPException(status_code=401, detail='Invalid Authorization header (not a bearer token)')
            return await self.validate(split_header[1]) 
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

token = TokenVerifier(
    origin=options.jwt_origin,
    audience=options.client_id,
    issuer=options.jwt_issuer,
    options={
        'require_aud': True,
        'require_iss': True,
    },
)

def staff(token: dict[str, Any] = Depends(token)):
    if token['intra-role'] != 'assistant' and token['intra-role'] != 'pedago':
        raise HTTPException(status_code=403)

def manager(token: dict[str, Any] = Depends(token)):
    if token['intra-role'] != 'pedago':
        raise HTTPException(status_code=403)
