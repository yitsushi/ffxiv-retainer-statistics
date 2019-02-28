import yaml, os, pathlib

class Config:
  __data = None

  def __init__(self):
    if os.getenv('RETAINER_CONFIG') is not None:
      path = os.getenv('RETAINER_CONFIG')
    else:
      path = f'{os.getenv("HOME")}/.config/ffxiv/app.yaml'

    f = open(path, 'r')
    self.__data = yaml.load(f)

  def retainer_ids(self):
    return self.__data['retainers'].keys()

  def retainer(self, id):
    return self.__data['retainers'][id]

  def character(self):
    return self.__data['character']
  
  def session_id(self):
    return self.__data['session']

  def data_dir(self):
    pathlib.Path(self.__data['data_directory']).mkdir(parents=True, exist_ok=True)
    return self.__data['data_directory']

  def log_dir(self):
    pathlib.Path(self.__data['log_directory']).mkdir(parents=True, exist_ok=True)
    return self.__data['log_directory']

  def sendgrid_token(self):
    return self.__data['sendgrid']['token']

  def sendgrid_to(self):
    return [{'email': r['email'], 'name': r['name']} for r in self.__data['sendgrid']['to']]

  def sendgrid_from(self):
    return self.__data['sendgrid']['from']

  def mailgun_api_key(self):
    return self.__data['mailgun']['api_key']

  def mailgun_domain(self):
    return self.__data['mailgun']['domain']

  def mailgun_from(self):
    f = self.__data['mailgun']['from']
    return f'{f["name"]} <{f["email"]}>'

  def mailgun_to(self):
    return [f"{to['name']} <{to['email']}>" for to in self.__data['mailgun']['to']]

  def xivapi_key(self):
    return self.__data['xivapi']['key']

  def xivapi_market(self):
    return self.__data['xivapi']['market']
