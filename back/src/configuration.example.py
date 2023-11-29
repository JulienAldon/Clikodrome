import pydantic
import os
import zoneinfo

class Configuration(pydantic.BaseSettings):
    frontend_uri:       str = 'http://localhost'
    public_uri:         str = 'http://localhost/api'
    timezone                = zoneinfo.ZoneInfo('Europe/Paris')

    jwt_origin:         str = os.getenv('JWT_ORIGIN')
    jwt_issuer:         str = os.getenv('JWT_ISSUER')

    client_id:          str = os.getenv('AZURE_CLIENT_ID')
    client_secret:      str = os.getenv('AZURE_CLIENT_SECRET')

    intranet_secret:    str = os.getenv('INTRANET_AUTOLOGIN')
    db_host:            str = os.getenv('DATABASE_HOST')
    db_user:            str = os.getenv('DATABASE_USER')
    db_password:        str = os.getenv('DATABASE_PASSWORD')
    database:           str = os.getenv('DATABASE_NAME')

    authorized_groups = ['pedago', 'assistants-wac-lyon']

    event_activity:     str = '/module/2021/W-ADM-007/LYN-0-1/acti-505014/'

    all_edusign_credentials = [
        {'login': os.getenv('EDUSIGN_LOGIN'), 'password': os.getenv('EDUSIGN_PASSWORD')},
    ]
    edusign_url:        str = 'https://api.edusign.fr'
    edusign_signature:  str = open('signature.txt').readline()


options = Configuration()