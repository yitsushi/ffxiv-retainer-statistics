import yaml
import os
import pathlib

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

    def db_type(self):
        try:
            return self.__data['database']['type']
        except KeyError:
            return 'sqlite'

    def database(self):
        return self.__data.get('database', None)

    def data_dir(self):
        pathlib.Path(
            self.__data['data_directory']).mkdir(
            parents=True, exist_ok=True)
        return self.__data['data_directory']

    def log_dir(self):
        pathlib.Path(
            self.__data['log_directory']).mkdir(
            parents=True,
            exist_ok=True)
        return self.__data['log_directory']

    def mailgun_api_key(self):
        return self.__data['mailgun']['api_key']

    def mailgun_domain(self):
        return self.__data['mailgun']['domain']

    def mailgun_from(self):
        f = self.__data['mailgun']['from']
        return f'{f["name"]} <{f["email"]}>'

    def mailgun_to(self):
        return [
            f"{to['name']} <{to['email']}>" for to in self.__data['mailgun']['to']]

