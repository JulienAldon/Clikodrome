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

    assistant_authorized_groups = ['assistants-wac-lyon']
    pedago_authorized_groups = ['pedago']

    bocal_url:          str = 'https://console.bocal.org'
    bocal_email:        str = os.getenv('BOCAL_EMAIL')
    bocal_password:     str = os.getenv('BOCAL_PASSWORD')
    edusign_url:        str = 'https://api.edusign.fr'

options = Configuration()