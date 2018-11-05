import yaml

class Config:
  __data = None

  def __init__(self):
    f = open('config/ffxiv.yaml', 'r')
    self.__data = yaml.load(f)

  def retainer_ids(self):
      return self.__data['retainers'].keys()

  def retainer(self, id):
      return self.__data['retainers'][id]

  def character(self):
      return self.__data['character']
  
  def session_id(self):
      return self.__data['session']
