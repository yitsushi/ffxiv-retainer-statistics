import json
import requests
from datetime import datetime
from .config import Config


class MailGun:
    def __init__(self):
        self.__config = Config()

    def send(self, text, html):
        requests.post(
            f'https://api.mailgun.net/v2/{self.__config.mailgun_domain()}/messages',
            auth=(
                'api',
                self.__config.mailgun_api_key()),
            data={
                "from": self.__config.mailgun_from(),
                "to": self.__config.mailgun_to(),
                "subject": f'[{str(datetime.now().date())}] FFXIV Retainer Statistics',
                "html": html,
                "text": text,
            })
