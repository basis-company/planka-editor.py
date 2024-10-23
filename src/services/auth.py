import os
import httpx
from dotenv import load_dotenv

load_dotenv()


def get_access_token() -> str:
    email_or_username = os.getenv('EMAIL_OR_USERNAME')
    if not email_or_username:
        raise ValueError('No value found for email_or_username')

    password = os.getenv('PLANKA_PASSWORD')
    if not password:
        raise ValueError('No value found for password')

    planka_host = os.getenv('PLANKA_HOST')
    if not planka_host:
        raise ValueError('No value found for planka_host')

    url = planka_host + '/api/access-tokens'
    data = {
        'emailOrUsername': email_or_username,
        'password': password
    }

    response = httpx.post(url, json=data)
    access_token = response.json()['item']

    return access_token
