import yaml, os

class Config:
  __data = None

  def __init__(self):
    f = open(f'{os.getenv("HOME")}/.config/ffxiv/app.yaml', 'r')
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
    return self.__data['data_directory']
  
  def log_dir(self):
    return self.__data['log_directory']

  def sendgrid_token(self):
    return self.__data['sendgrid']['token']

  def sendgrid_to(self):
    return [{'email': r['email'], 'name': r['name']} for r in self.__data['sendgrid']['to']]

  def sendgrid_from(self):
    return {
      'email': self.__data['sendgrid']['from']['email'],
      'name': self.__data['sendgrid']['from']['name'],
    }
