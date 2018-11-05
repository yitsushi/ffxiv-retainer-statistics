from .config import Config
import requests, json

class SendGrid:
  def __init__(self):
    self.__config = Config()
  
  def send(self, content):
    headers = {
      'authorization': f'Bearer {self.__config.sendgrid_token()}',
      'content-type': 'application/json'
    }
    payload = {
      'personalizations': [{
          'to': self.__config.sendgrid_to(),
          'subject': 'FFXIV Retainer Statistics',
      }],
      'content': [
        {'type': 'text/html', 'value': content}
      ],
      'from': self.__config.sendgrid_from(),
    }
    requests.post(
      'https://api.sendgrid.com/v3/mail/send',
      data=json.dumps(payload, ensure_ascii=False),
      headers=headers
    )
