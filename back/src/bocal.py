import aiohttp
from src.configuration import options

async def card_login():
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{options.bocal_url}/auth/login', headers={
            'Content-Type': 'application/json',}, json={'id': options.bocal_email, 'password': options.bocal_password}
        ) as resp:
            result = await resp.json()
            if not result.get('token'):
                raise KeyError('Token not found.')
        return result['token']

async def get_card_information(_id, token):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{options.bocal_url}/api/cards/{_id}', headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }) as resp:
            result = await resp.json()
            if not result.get('card'):
                KeyError('Card not found')
        return result

async def get_user_information(login, token):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{options.bocal_url}/api/epitech.eu/users/{login}', headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }) as resp:
            result = await resp.json()
            if not result.get('card_id'):
                KeyError('User not registered to bocal access control')
        return result