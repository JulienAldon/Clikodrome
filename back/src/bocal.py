import aiohttp
from src.configuration import options
import datetime

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
                raise KeyError('Card not found')
        return result

async def get_user_information(login, token):
    """Get latest card ID from a login.

    Args:
        login (String): Login of the student.
        token (String): Bocal token.

    Raises:
        KeyError: User not registered to bocal access control can be raised by this function.

    Returns:
        dict: object containing the `card` and the `assigned_date`.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{options.bocal_url}/api/epitech.eu/users/{login}/card', headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }) as resp:
            result = await resp.json()
            if result == []:
                raise KeyError('User not registered to bocal access control')
        result = sorted(result, key=lambda x: datetime.datetime.strptime(x['assigned_date'], '%d-%m-%Y %H:%M:%S'))
        return result[-1]