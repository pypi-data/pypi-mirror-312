
import yaml

from easy_api_test.core.models import Model


class ConfigReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self):
        pass

class YamlConfigReader(ConfigReader):
    def read(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)


class BaseSetting(Model):

    @classmethod
    def load_from_yaml_file(cls, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            return cls.from_dict(yaml.safe_load(f))
    
    @classmethod
    def load_from_data(cls, data: dict):
        return cls.from_dict(data)
